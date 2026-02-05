import frappe
from frappe.utils import getdate, nowdate, add_days, fmt_money
import json

@frappe.whitelist()
def get_customer_sidebar_data():
    try:
        user_email = frappe.session.user
        customer = frappe.db.get_value("Customer", {"email_id": user_email}, "name") or \
                   frappe.db.get_value("Customer", {"user": user_email}, "name")

        final_pincode_list = []
        if customer:
            cust_addr_names = frappe.get_all("Dynamic Link", 
                filters={"link_doctype": "Customer", "link_name": customer, "parenttype": "Address"}, 
                pluck="parent")
            if cust_addr_names:
                addresses = frappe.get_all("Address", filters={"name": ["in", cust_addr_names]}, fields=["pincode", "is_primary_address"])
                primary_pins = [a.pincode for a in addresses if a.is_primary_address and a.pincode]
                other_pins = [a.pincode for a in addresses if not a.is_primary_address and a.pincode]
                final_pincode_list = sorted(list(set(primary_pins)), reverse=True) + sorted(list(set(other_pins) - set(primary_pins)))

        if not final_pincode_list and user_email == "Administrator":
            final_pincode_list = ["388001"]

        if not final_pincode_list: return {"status": "error", "message": "No Pincodes found."}

        societies = frappe.get_all("Company", filters={"custom_society": 1}, pluck="name")
        sellers = frappe.get_all("Company", filters={"custom_seller": 1}, pluck="name")

        addr_list = frappe.get_all("Address", filters={"pincode": ["in", final_pincode_list]}, fields=["name", "pincode"])
        addr_map = {d.name: d.pincode for d in addr_list}
        
        def get_companies_at_addresses(company_list):
            if not company_list or not addr_list: return {}
            links = frappe.get_all("Dynamic Link", filters={"link_doctype": "Company", "link_name": ["in", company_list], "parent": ["in", list(addr_map.keys())]}, fields=["link_name", "parent"])
            mapping = {}
            for l in links:
                pin = addr_map.get(l.parent)
                if pin:
                    if pin not in mapping: mapping[pin] = []
                    if l.link_name not in mapping[pin]: mapping[pin].append(l.link_name)
            return mapping

        pin_soc_map = get_companies_at_addresses(societies)
        pin_sell_map = get_companies_at_addresses(sellers)

        all_items_raw = frappe.get_all("Item", filters={"disabled": 0, "is_sales_item": 1}, fields=["item_code", "item_name", "item_group", "image", "description"])
        today_date = nowdate()
        pricing_day = getdate(today_date).strftime("%A")
        territory = frappe.db.get_value("Customer", {"user": user_email}, "territory") or "All Territories"

        processed_items = []
        for item in all_items_raw:
            price = find_price_recursive(item.item_code, territory, pricing_day, today_date)
            processed_items.append({
                "item_code": item.item_code, "item_name": item.item_name, "item_group": item.item_group,
                "image": item.image, "short_description": (item.description or "")[:65] + "...",
                "price": price, "formatted_price": fmt_money(price, currency="INR")
            })

        final_data = []
        for pin in final_pincode_list:
            sellers_at_pin = pin_sell_map.get(pin, [])
            categories_list = []
            if sellers_at_pin:
                grouped_items = {}
                for item in processed_items:
                    cat = item["item_group"]
                    if cat not in grouped_items: grouped_items[cat] = []
                    grouped_items[cat].append(item)
                for cat, items in grouped_items.items():
                    categories_list.append({"name": cat, "sellers": [{"name": s, "items": items} for s in sellers_at_pin]})
            soc_objs = [{"name": soc, "categories": categories_list} for soc in pin_soc_map.get(pin, [])]
            final_data.append({"pincode": pin, "societies": soc_objs})

        return {"status": "success", "data": final_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_price_recursive(item_code, current_territory, day, target_date):
    while current_territory:
        rules = frappe.get_all("Daily Item Price", filters={"item_code": item_code, "territory": current_territory}, fields=["name", "start_date"], order_by="start_date desc")
        for r in rules:
            if r.start_date <= getdate(target_date):
                price = frappe.db.get_value("Daily Price Detail", {"parent": r.name, "day": day}, "price")
                if price: return price
        current_territory = frappe.db.get_value("Territory", current_territory, "parent_territory")
    return 0.0

@frappe.whitelist()
def place_custom_order(cart_items, seller_company):
    try:
        items = json.loads(cart_items)
        if not items: return {"status": "error", "message": "Cart is empty"}

        customer = frappe.db.get_value("Customer", {"user": frappe.session.user}, "name")
        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.company = seller_company
        so.delivery_date = add_days(nowdate(), 1)
        
        for itm in items:
            so.append("items", {
                "item_code": itm['item_code'],
                "qty": itm['qty'],
                "rate": itm['price'],
                "delivery_date": so.delivery_date
            })
        
        so.insert(ignore_permissions=True)
        so.submit()
        return {"status": "success", "order_name": so.name}
    except Exception as e:
        frappe.log_error("Order Error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def get_my_orders():
    try:
        user = frappe.session.user
        customer = frappe.db.get_value("Customer", {"user": user}, "name")
        if not customer: return []

        orders = frappe.get_all("Sales Order", 
            filters={"customer": customer},
            fields=["name", "grand_total", "status", "transaction_date", "delivery_date", "docstatus", "company"],
            order_by="creation desc"
        )

        for order in orders:
            order_items = frappe.db.get_all("Sales Order Item",
                filters={"parent": order.name},
                fields=["item_code", "item_name", "qty", "rate", "amount"]
            )
            for item in order_items:
                item["image"] = frappe.db.get_value("Item", item.item_code, "image")
            order["items"] = order_items
            
        return orders
    except Exception as e:
        frappe.log_error("API Error", str(e))
        return []

@frappe.whitelist()
def cancel_custom_order(order_name):
    try:
        user = frappe.session.user
        customer = frappe.db.get_value("Customer", {"user": user}, "name")
        order = frappe.get_doc("Sales Order", order_name)
        
        if order.customer != customer:
             return {"status": "error", "message": "Unauthorized"}
        if order.docstatus == 2:
            return {"status": "error", "message": "Already cancelled."}
        if order.status == "Completed":
             return {"status": "error", "message": "Cannot cancel completed order."}

        order.flags.ignore_permissions = True
        order.cancel()
        return {"status": "success", "message": "Order cancelled."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def delete_custom_order(order_name):
    try:
        user = frappe.session.user
        customer = frappe.db.get_value("Customer", {"user": user}, "name")
        order = frappe.get_doc("Sales Order", order_name)
        
        if order.customer != customer:
             return {"status": "error", "message": "Unauthorized"}
    
        if order.docstatus == 1:
             return {"status": "error", "message": "Cannot delete submitted order. Cancel it first."}

        frappe.delete_doc("Sales Order", order_name)
        return {"status": "success", "message": "Order deleted."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_user_role_info():
    """Checks role and returns redirection info"""
    user = frappe.session.user
    if user == "Guest":
        return {"role": "Guest"}

    roles = frappe.get_roles(user)

    if "Seller" in roles:
        # Check User Permission for Company
        seller_company = frappe.db.get_value("User Permission", 
            {"user": user, "allow": "Company"}, "for_value")
        
        if seller_company:
            return {
                "role": "Seller",
                "company": seller_company,
                "redirect": "/seller"
            }
    
    # Default to Customer
    return {
        "role": "Customer",
        "redirect": "/"
    }

@frappe.whitelist()
def get_seller_orders():
    """Fetch orders specifically for the logged-in Seller's Company"""
    user = frappe.session.user
    
    # 1. Get Company from Permission
    seller_company = frappe.db.get_value("User Permission", 
            {"user": user, "allow": "Company"}, "for_value")
    
    if not seller_company:
        return []

    # 2. Fetch Orders for that Company
    orders = frappe.get_all("Sales Order",
        filters={"company": seller_company},
        fields=["name", "customer_name", "grand_total", "status", "transaction_date"],
        order_by="creation desc"
    )

    # 3. Fetch Items
    for order in orders:
        order["items"] = frappe.get_all("Sales Order Item",
            filters={"parent": order.name},
            fields=["item_code", "item_name", "qty", "amount"]
        )
    
    return orders

@frappe.whitelist()
def update_order_status(order_name, status):
    """Allow Seller to update status if order belongs to their company"""
    try:
        user = frappe.session.user
        seller_company = frappe.db.get_value("User Permission", 
            {"user": user, "allow": "Company"}, "for_value")
        
        doc = frappe.get_doc("Sales Order", order_name)
        
        # Security Check
        if doc.company != seller_company:
            return {"status": "error", "message": "Unauthorized access"}

        if status == 'Completed':
            doc.db_set('status', 'Completed')
        else:
            doc.db_set('status', status)
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



        