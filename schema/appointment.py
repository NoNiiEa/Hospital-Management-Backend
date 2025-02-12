def individual_schema(appointment):
    return {
        "id": str(appointment["_id"]),
        "patient_id": str(appointment.get("patient_id", "N/A")),
        "doctor_id": str(appointment.get("doctor_id", "N/A")),
        "date": appointment.get("date", "N/A"),
        "time": appointment.get("time", "N/A"),
        "status": appointment.get("status", "N/A")
    }

def list_schema(appointments):
    return [individual_schema(appointment) for appointment in appointments]