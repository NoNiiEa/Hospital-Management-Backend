def individual_patient_schema(patient):
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", "N/A"),
        "age": patient.get("age", "N/A"),
        "gender": patient.get("gender", "N/A"),
        "contact": {
            "phone": patient.get("contact", {}).get("phone", "N/A"),
            "email": patient.get("contact", {}).get("email", "N/A"),
            "address": patient.get("contact", {}).get("address", "N/A")
        },
        "medical_history": [
            {
                "disease": history.get("disease", "N/A"),
                "diagnosed_date": history.get("diagnosed_date", "N/A"),
                "treatment": history.get("treatment", "N/A")
            }
            for history in patient.get("medical_history", [])
        ],
        "appointments": [str(appointment) for appointment in patient.get("appointments", [])],
        "prescriptions": [str(prescription) for prescription in patient.get("prescriptions", [])]
    }


def list_patient_schema(patients):
    return [individual_patient_schema(patient) for patient in patients]
