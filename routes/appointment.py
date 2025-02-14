from fastapi import APIRouter, HTTPException
from models.appointment import AppointmentModel, UpdateStatusRequest
from config.database import appointments as appointment_collection, patients as patient_collection, doctors as doctor_collection
from schema.appointment import list_schema
from bson import ObjectId
from starlette import status

appointment_router = APIRouter()

@appointment_router.get("/")
async def get_appointments():
    appointments = appointment_collection.find()
    return list_schema(appointments)

@appointment_router.post("/create")
async def create_appointments(appointment: AppointmentModel):
    json = appointment.model_dump()
    response = appointment_collection.insert_one(json)

    patient_id = json["patient_id"]
    doctor_id = json["doctor_id"]

    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Patient ID")
    if not ObjectId.is_valid(doctor_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Doctor ID")
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id: {doctor_id} not found.")

    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
    doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
    if patient:
        old_appointments = patient["appointments"]
        old_appointments.append(str(response.inserted_id))
        result = patient_collection.update_one(
            {'_id': ObjectId(patient_id)},
            {"$set": {'appointments': old_appointments}}
        )
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id: {patient_id} not found.")
    return {"id": str(response.inserted_id)}

@appointment_router.delete("/delete/{appointment_id}")
async def delete_appointment(appointment_id: str):
    try:
        appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

        patient_id = appointment["patient_id"]

        result = appointment_collection.delete_one({"_id": ObjectId(appointment_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete appointment")

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if patient and "appointments" in patient:
            list_appointment = patient["appointments"]
            if str(appointment_id) in list_appointment:
                list_appointment.remove(str(appointment_id))

            patient_collection.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": {"appointments": list_appointment}}
            )

        return {"result": "Appointment has been successfully deleted"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@appointment_router.patch("/{appointment_id}/status")
async def update_appointment_status(appointment_id: str, status_update: UpdateStatusRequest):
    new_status = status_update.status
    
    try:
        appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

        result = appointment_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": new_status}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update appointment status")

        return {"message": "Appointment status updated successfully", "status": new_status}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    
