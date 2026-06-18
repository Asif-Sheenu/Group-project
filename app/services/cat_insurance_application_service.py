from app.models.cat_insurance_application import (
    CatInsuranceApplication
)


def create_application(db, application_data):

    application = CatInsuranceApplication(

        user_id=1,

        plan_name=application_data.plan_name,

        cat_name=application_data.cat_name,

        breed=application_data.breed,

        age=application_data.age,

        gender=application_data.gender,

        weight=application_data.weight,

        vaccination_status=application_data.vaccination_status,

        existing_disease=application_data.existing_disease,

        front_image=application_data.front_image,

        side_image=application_data.side_image,

        full_body_image=application_data.full_body_image,

        vaccination_proof=application_data.vaccination_proof,

        medical_record=application_data.medical_record,

        status="pending"
    )

    db.add(application)

    db.commit()

    db.refresh(application)

    return application