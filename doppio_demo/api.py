import frappe
from frappe.utils import getdate, nowdate, add_days, fmt_money
import json

@frappe.whitelist(allow_guest=True)
def logout():
    frappe.local.login_manager.logout()
    frappe.db.commit()
    return {"status": "success"}

# --- CUSTOMER SIDEBAR & PRICING ---
@frappe.whitelist()
def get_customer_sidebar_data():
    try:
        user_email = frappe.session.user
        customer = frappe.db.get_value("Customer", {"email_id": user_email}, "name") or \
                   frappe.db.get_value("Customer", {"user": user_email}, "name")

        final_pincode_list = []
        if customer:
            cust_addr_names = frappe.get_all("Dynamic Link", filters={"link_doctype": "Customer", "link_name": customer, "parenttype": "Address"}, pluck="parent")
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
    return frappe.db.get_value("Item Price", {"item_code": item_code, "price_list": "Standard Selling"}, "price_list_rate") or 0.0

# --- SELLER LOGIC ---
@frappe.whitelist()
def get_seller_sidebar_data():
    try:
        user = frappe.session.user
        seller_company = frappe.db.get_value("User Permission", {"user": user, "allow": "Company"}, "for_value")
        if not seller_company:
             seller_company = frappe.db.get_value("Company", {"custom_seller": 1}, "name")

        if not seller_company: return {"status": "error", "message": "No Shop assigned."}

        seller_pincodes = [] 
        primary_pincode = None
        seller_addrs = frappe.get_all("Dynamic Link", filters={"link_doctype": "Company", "link_name": seller_company, "parenttype": "Address"}, pluck="parent")
        
        if seller_addrs:
            addresses = frappe.get_all("Address", filters={"name": ["in", seller_addrs]}, fields=["pincode", "is_primary_address"])
            for addr in addresses:
                if addr.pincode:
                    seller_pincodes.append(addr.pincode)
                    if addr.is_primary_address: primary_pincode = addr.pincode
        
        if not seller_pincodes: return {"status": "error", "message": "Seller has no Pincode defined."}

        orders = frappe.get_all("Sales Order", 
            filters={
                "company": seller_company,
                "docstatus": ["<", 2], 
                "status": ["not in", ["Cancelled", "Completed", "Closed"]] 
            },
            fields=["name", "customer", "customer_name", "shipping_address_name", "customer_address"]
        )

        tree_structure = {}
        for order in orders:
            addr_name = order.shipping_address_name or order.customer_address
            order_pincode = None
            society = "Unknown Area"

            if addr_name:
                addr_doc = frappe.db.get_value("Address", addr_name, ["pincode", "address_line2", "city"], as_dict=True)
                if addr_doc:
                    order_pincode = addr_doc.pincode
                    if addr_doc.address_line2: society = addr_doc.address_line2
                    elif addr_doc.city: society = addr_doc.city

            if not order_pincode or order_pincode not in seller_pincodes: continue 

            items = frappe.get_all("Sales Order Item", filters={"parent": order.name}, fields=["item_group"])
            if not items: items = [{"item_group": "General"}]

            for item in items:
                category = item.item_group or "General"
                if order_pincode not in tree_structure: tree_structure[order_pincode] = {}
                if society not in tree_structure[order_pincode]: tree_structure[order_pincode][society] = {}
                if category not in tree_structure[order_pincode][society]: tree_structure[order_pincode][society][category] = []
                
                cust_list = tree_structure[order_pincode][society][category]
                if not any(c['name'] == order.customer_name for c in cust_list):
                    cust_list.append({"name": order.customer_name})

        final_data = []
        sorted_pins = sorted(tree_structure.keys(), key=lambda x: (x != primary_pincode, x))

        for pin in sorted_pins:
            soc_list = []
            for soc in sorted(tree_structure[pin].keys()):
                cat_list = []
                for cat in sorted(tree_structure[pin][soc].keys()):
                    customers = sorted(tree_structure[pin][soc][cat], key=lambda x: x['name'])
                    cat_list.append({"name": cat, "customers": customers})
                soc_list.append({"name": soc, "categories": cat_list})
            
            final_data.append({"pincode": pin, "societies": soc_list, "is_primary": (pin == primary_pincode)})

        return {"status": "success", "data": final_data}
    except Exception as e: return {"status": "error", "message": str(e)}

@frappe.whitelist()
def get_seller_orders(customer_name=None):
    user = frappe.session.user
    seller_company = frappe.db.get_value("User Permission", {"user": user, "allow": "Company"}, "for_value")
    if not seller_company: seller_company = frappe.db.get_value("Company", {"custom_seller": 1}, "name")

    filters = {"company": seller_company, "docstatus": ["<", 2]}
    if customer_name: filters["customer_name"] = customer_name

    orders = frappe.get_all("Sales Order", 
        filters=filters, 
        fields=["name", "customer_name", "grand_total", "status", "transaction_date", "docstatus", "per_delivered", "per_billed"], 
        order_by="creation desc"
    )
    for order in orders:
        order["items"] = frappe.db.sql("""
            SELECT soi.item_code, soi.item_name, soi.qty, soi.amount, itm.image 
            FROM `tabSales Order Item` soi
            LEFT JOIN `tabItem` itm ON soi.item_code = itm.name
            WHERE soi.parent = %s
        """, (order.name,), as_dict=1)
    return orders

# --- CUSTOMER GET ORDERS ---
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
            order_items = frappe.db.get_all("Sales Order Item", filters={"parent": order.name}, fields=["item_code", "item_name", "qty", "rate", "amount"])
            for item in order_items:
                item["image"] = frappe.db.get_value("Item", item.item_code, "image")
            order["items"] = order_items
        return orders
    except Exception as e: return []

# --- ACTIONS ---
@frappe.whitelist()
def update_order_status(order_name, status):
    try:
        doc = frappe.get_doc("Sales Order", order_name)
        if doc.docstatus == 0: doc.submit()
        return {"status": "success", "message": "Order Accepted"}
    except Exception as e: return {"status": "error", "message": str(e)}

@frappe.whitelist()
def cancel_custom_order(order_name):
    try:
        # 1. Fetch the Order
        doc = frappe.get_doc("Sales Order", order_name)

        # 2. Security: Verify the order belongs to this customer
        # We don't want customers canceling random orders if they guess the ID
        user_customer = frappe.db.get_value("Customer", {"user": frappe.session.user}, "name")
        if doc.customer != user_customer and frappe.session.user != "Administrator":
             return {"status": "error", "message": "You do not have permission to cancel this order."}

        # 3. Cancel with PERMISSION BYPASS
        if doc.docstatus == 1:
            doc.flags.ignore_permissions = True # <--- This is the key fix
            doc.cancel()
            return {"status": "success", "message": "Order Cancelled"}
        
        return {"status": "error", "message": "Order is not in a cancellable state."}
    except Exception as e: return {"status": "error", "message": str(e)}

@frappe.whitelist()
def delete_custom_order(order_name):
    try:
        docstatus = frappe.db.get_value("Sales Order", order_name, "docstatus")
        # Security check
        owner = frappe.db.get_value("Sales Order", order_name, "owner")
        if owner != frappe.session.user and frappe.session.user != "Administrator":
            return {"status": "error", "message": "You can only delete your own orders."}

        if docstatus in [0, 2]: # Draft or Cancelled
            frappe.delete_doc("Sales Order", order_name, ignore_permissions=True) # <--- Already fixed here
            return {"status": "success", "message": "Order Deleted"}
        else:
            return {"status": "error", "message": "Cannot delete a submitted order. Cancel it first."}
    except Exception as e: return {"status": "error", "message": str(e)}

@frappe.whitelist()
def place_custom_order(cart_items, seller_company):
    try:
        items = json.loads(cart_items)
        customer = frappe.db.get_value("Customer", {"user": frappe.session.user}, "name")
        address_name = frappe.db.get_value("Dynamic Link", {"link_doctype": "Customer", "link_name": customer, "parenttype": "Address"}, "parent")
        
        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.company = seller_company
        so.delivery_date = add_days(nowdate(), 1)
        if address_name: so.shipping_address_name = address_name; so.customer_address = address_name
        
        for itm in items: 
            so.append("items", {"item_code": itm['item_code'], "qty": itm['qty'], "rate": itm['price'], "delivery_date": so.delivery_date})
        
        so.insert(ignore_permissions=True)
        return {"status": "success", "order_name": so.name}
    except Exception as e: return {"status": "error", "message": str(e)}

@frappe.whitelist()
def get_user_role_info():
    user = frappe.session.user
    if user == "Guest": return {"role": "Guest", "redirect": "/login"}
    roles = frappe.get_roles(user)
    if "Seller" in roles:
        company = frappe.db.get_value("User Permission", {"user": user, "allow": "Company"}, "for_value")
        if not company: company = frappe.db.get_value("Company", {"custom_seller": 1}, "name")
        return {"role": "Seller", "company": company, "redirect": "/seller"}
    return {"role": "Customer", "redirect": "/"}