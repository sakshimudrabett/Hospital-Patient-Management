from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.model_patient import Patient


client = TestClient(app)


def _clear_patients():
    db = SessionLocal()
    try:
        db.query(Patient).delete()
        db.commit()
    finally:
        db.close()


def test_create_patient_rest_endpoint():
    _clear_patients()
    payload = {
        "first_name": "Ava",
        "last_name": "Stone",
        "age": 29,
        "gender": "female",
    }

    response = client.post("/patients/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "Patient stored"
    assert isinstance(body["patient_id"], int)


def test_list_patients_returns_created_item():
    _clear_patients()
    client.post(
        "/patients/",
        json={
            "first_name": "Noah",
            "last_name": "Lee",
            "age": 35,
            "gender": "male",
        },
    )

    response = client.get("/patients/")
    assert response.status_code == 200
    patients = response.json()
    assert len(patients) == 1
    assert patients[0]["first_name"] == "Noah"
    assert patients[0]["last_name"] == "Lee"


def test_get_patient_by_id():
    _clear_patients()
    create_response = client.post(
        "/patients/",
        json={
            "first_name": "Mia",
            "last_name": "Khan",
            "age": 31,
            "gender": "female",
        },
    )
    patient_id = create_response.json()["patient_id"]

    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    patient = response.json()
    assert patient["id"] == patient_id
    assert patient["first_name"] == "Mia"


def test_get_missing_patient_returns_404():
    _clear_patients()
    response = client.get("/patients/999999")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HTTP_ERROR"
    assert error["message"] == "Patient not found."


def test_patch_patient_updates_selected_fields():
    _clear_patients()
    create_response = client.post(
        "/patients/",
        json={
            "first_name": "Ella",
            "last_name": "West",
            "age": 40,
            "gender": "female",
        },
    )
    patient_id = create_response.json()["patient_id"]

    response = client.patch(
        f"/patients/{patient_id}",
        json={"age": 41, "last_name": "Wells"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == patient_id
    assert body["first_name"] == "Ella"
    assert body["last_name"] == "Wells"
    assert body["age"] == 41


def test_delete_patient_removes_record():
    _clear_patients()
    create_response = client.post(
        "/patients/",
        json={
            "first_name": "Liam",
            "last_name": "Cole",
            "age": 33,
            "gender": "male",
        },
    )
    patient_id = create_response.json()["patient_id"]

    delete_response = client.delete(f"/patients/{patient_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Patient deleted"}

    get_response = client.get(f"/patients/{patient_id}")
    assert get_response.status_code == 404


def test_patch_missing_patient_returns_404():
    _clear_patients()
    response = client.patch("/patients/999999", json={"age": 55})
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HTTP_ERROR"
    assert error["message"] == "Patient not found."


def test_delete_missing_patient_returns_404():
    _clear_patients()
    response = client.delete("/patients/999999")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "HTTP_ERROR"
    assert error["message"] == "Patient not found."


def test_legacy_create_route_removed():
    _clear_patients()
    response = client.post(
        "/patients/create",
        json={
            "first_name": "Old",
            "last_name": "Route",
            "age": 30,
            "gender": "female",
        },
    )
    assert response.status_code == 405


def test_seed_demo_replaces_with_three_records():
    _clear_patients()
    client.post(
        "/patients/",
        json={
            "first_name": "Temp",
            "last_name": "Entry",
            "age": 50,
            "gender": "male",
        },
    )

    seed_response = client.post("/patients/seed-demo")
    assert seed_response.status_code == 201
    assert seed_response.json() == {"message": "Demo patients seeded", "count": 3}

    list_response = client.get("/patients/")
    assert list_response.status_code == 200
    patients = list_response.json()
    assert len(patients) == 3
