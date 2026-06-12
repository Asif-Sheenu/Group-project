from pydantic import BaseModel

class HospitalCreate(BaseModel):
    hospital_name: str
    registration_number: str
    contact_person: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    password: str

    confirm_password: str

    website_url: str | None = None
    google_maps_url: str | None = None

class HospitalResponse(BaseModel):
    id: int
    hospital_name: str
    registration_number: str

    class Config:
        from_attributes = True    


class HospitalLogin(BaseModel):
    registration_number: str
    password: str