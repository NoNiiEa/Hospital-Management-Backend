def individual_schema(prescription):
    return {
        "id": str(prescription["_id"]),
        "patientID": str(prescription.get("patientID", "N/A")),
        "doctorID": str(prescription.get("doctorID", "N/A")),
        "date": prescription.get("date", "N/A"),
        "medications": [
            {
                "name": medication.get("name", "N/A"),
                "dosage": medication.get("dosage", "N/A"),
                "frequency": medication.get("frequency", "N/A"),
                "duration": medication.get("duration", "N/A"),
            }
            for medication in prescription.get("medications", [])
        ],
    }

def list_schema(prescriptions):
    return [individual_schema(prescription) for prescription in prescriptions]