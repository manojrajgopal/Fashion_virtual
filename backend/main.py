from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import tryon, auth, gallery
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tryon.router, prefix="/api")
app.include_router(auth.router, prefix ="/api")
app.include_router(gallery.router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "Okay",
        "message": "Fashion Virtual Backend is running"
    }
