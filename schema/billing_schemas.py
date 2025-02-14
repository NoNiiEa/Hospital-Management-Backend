from bson import ObjectId

def individual_billing_schema(billing):
    return {
        "id": str(billing["_id"]),
        "patient": billing.get("patient_id","N\A"),
        "appointment": billing.get("appointment_id","N\A"),
        "total_amount": billing.get("total_amount", "N/A"),
        "payment_method":billing.get("payment_method", "N/A")
        
    }

def list_billing_schema(billings):
    return [individual_billing_schema(billing) for billing in billings]
