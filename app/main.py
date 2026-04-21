from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import appointment
from app.database import Base, engine
from app.routers import patient

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
# Create tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(patient.router, prefix="/patients", tags=["Patients"])


@app.get("/")
def root():
    return {"message": "API Running"}