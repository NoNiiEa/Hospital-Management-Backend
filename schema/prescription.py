def individual_schema(prescription):
    return {
        "id": str(prescription["_id"]),
        "patient_id": prescription.get("patient_id", "N/A"),
        "doctor_id": prescription.get("doctor_id", "N/A"),
        "date": prescription.get("date", "N/A"),
        "medications": [
            {
                "name": medication.get("name", "N/A"),
                "dosage": medication.get("dosage", "N/A"),
                "frequency": medication.get("frequency", "N/A"),
                "duration": medication.get("duration", "N/A")
            }
            for medication in prescription.get("medications", [])
        ]
    }

def list_schema(prescriptions):
    return [individual_schema(prescription) for prescription in prescriptions]