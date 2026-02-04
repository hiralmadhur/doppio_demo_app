import frappe
from frappe.utils import getdate, nowdate, add_days, fmt_money

@frappe.whitelist()
def redirect_to_app(user=None):
    if not user: user = frappe.session.user
    roles = frappe.get_roles(user)
    if "Customer" in roles and "System Manager" not in roles:
        return "/doppiodemo"
    return "/app"

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
        import json
        items = json.loads(cart_items) # Frontend se list aayegi
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


import frappe

@frappe.whitelist()
def get_my_orders():
    try:
        user = frappe.session.user
        # Customer fetch karein
        customer = frappe.db.get_value("Customer", {"user": user}, "name")
        
        if not customer:
            return [] # Empty list return karein agar customer nahi hai

        # Orders fetch karein
        orders = frappe.get_all("Sales Order", 
            filters={"customer": customer, "docstatus": ["!=", 2]}, # Cancelled orders chhod kar
            fields=["name", "grand_total", "status", "transaction_date", "delivery_date"],
            order_by="creation desc"
        )

        for order in orders:
            # Har order ke items fetch karein
            order_items = frappe.db.get_all("Sales Order Item",
                filters={"parent": order.name},
                fields=["item_code", "item_name", "qty", "rate", "amount"]
            )
            
            # IMPORTANT: Item Master se Image fetch karein (Kyunki Sales Order Item me image nahi hoti)
            for item in order_items:
                item["image"] = frappe.db.get_value("Item", item.item_code, "image")

            order["items"] = order_items
            
        return orders # ❌ Pehle hum dict return kar rahe the, ✅ Ab seedha LIST return kar rahe hain

    except Exception as e:
        frappe.log_error("API Error", str(e))
        return []