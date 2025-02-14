def individual_schema(staff):
    return {
        "name": staff.get("name", "N/A"),
        "role": staff.get("role", "N/A"),
        "contact": {
            "phone": staff.get("contact", {}).get("phone", "N/A"),
            "email": staff.get("contact", {}).get("email", "N/A"),
            "address": staff.get("contact", {}).get("address", "N/A")
        },
        "shift": staff.get("shift", "N/A")
    }

def list_schema(staffs):
    return [individual_schema(staff) for staff in staffs]