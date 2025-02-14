from pydantic import BaseModel

class ContactModel(BaseModel):
    phone: str
    email: str
    address: str

class StaffModel(BaseModel):
    name: str
    role: str
    contact: ContactModel
    shift: str
