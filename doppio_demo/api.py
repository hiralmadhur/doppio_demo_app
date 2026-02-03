import frappe

@frappe.whitelist(allow_guest=True)
def get_hyperlocal_data():
    try:
        # 1. Fetch Societies
        societies = frappe.get_all("Society", fields=["name", "pincode"])
        
        # 2. Fetch Marketplace Data (Using ORM - No Raw SQL)
        marketplace = []

        # Step A: Wo saare Address nikalo jo Companies ke hain
        company_addresses = frappe.get_all("Address", 
            filters={
                "is_your_company_address": 1, 
                "link_doctype": "Company" # Sirf Company wale address
            }, 
            fields=["pincode", "link_name as company"]
        )

        for addr in company_addresses:
            # Step B: Har Company ke liye Categories nikalo (Child Table se)
            # Note: Yahan 'Company Supported Category' aapke Child Doctype ka naam hai
            categories = frappe.get_all("Company Supported Category", 
                filters={"parent": addr.company}, 
                fields=["category"]
            )
            
            # Step C: Company ka asli naam (Label) nikalo
            company_label = frappe.db.get_value("Company", addr.company, "company_name")

            # Step D: List me add karo
            for cat in categories:
                marketplace.append({
                    "pincode": addr.pincode,
                    "company_name": addr.company,
                    "company_label": company_label,
                    "category": cat.category
                })

        return {
            "societies": societies,
            "marketplace": marketplace
        }

    except Exception as e:
        # Agar koi error aaye to Server Crash mat karo, Error message bhejo
        frappe.log_error(f"Hyperlocal API Error: {str(e)}")
        return {"error": str(e), "societies": [], "marketplace": []}