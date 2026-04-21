# 🏥 Hospital Management System

A full-stack Hospital Management System built to manage patients, appointments, and hospital workflows efficiently.  
This project demonstrates backend API design, frontend integration, and real-world system logic.

---
Deployed Link : https://hospital-patient-managemnt.netlify.app/
---

## 🚀 Features

### 👤 Patient Management
- Create, update, and delete patients
- View all patients in a structured table
- Search patients by name
- Maintain patient records

---

### 📅 Appointment Management
- Schedule appointments for patients
- Assign doctors to appointments
- Track appointment date and time
- Update appointment status:
  - Scheduled
  - Completed
  - Cancelled

---

### 🔗 Patient History (Key Feature)
- Click a patient to view all their past appointments
- Track visit history
- Monitor treatment flow

---

### 🔄 Real-Time Updates
- Dynamic UI updates without page reload
- Status updates reflected instantly
- Clean and responsive workflow

---

## 🧠 System Workflow

1. Receptionist creates a patient
2. Appointment is scheduled for the patient
3. Doctor handles the appointment
4. Appointment status is updated
5. Patient history is maintained

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**

### Frontend
- **HTML**
- **CSS**
- **JavaScript (Vanilla JS)**

### Deployment
- Backend: Render
- Frontend: Netlify

---

## 📂 Project Structure
app/
├── models/
│ ├── model_patient.py
│ ├── model_appointment.py
│
├── schemas/
│ ├── patient.py
│ ├── appointment.py
│
├── routers/
│ ├── patient.py
│ ├── appointment.py
│
├── database.py
├── main.py

frontend/
├── index.html
├── styles.css
├── app.js


---


---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/hospital-management-system.git
cd
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run backend
```bash
uvicorn app.main:app --reload
```

### 5. Run frontend
Open `index.html` using Live Server or browser.

---

## 🌐 API Documentation

Once backend is running:

👉 http://127.0.0.1:8000/docs

Interactive Swagger UI available.

---

## 📸 Screenshots (Add later)

- Patient List
- Appointment Table
- Patient History

---

## 🎯 Key Highlights

- Full-stack CRUD application
- Real-world hospital workflow simulation
- REST API design using FastAPI
- Clean separation of backend & frontend
- Interactive UI with dynamic updates

---

## 🚀 Future Improvements

- 🔐 Role-based authentication (Admin / Doctor / Receptionist)
- 📊 Dashboard with analytics
- 📅 Appointment conflict handling
- ☁️ PostgreSQL integration for production
- 📂 File upload for medical records

---

## 👩‍💻 Author

**Sakshi C Mudrabett**

```

