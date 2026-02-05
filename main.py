from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router

app = FastAPI(title="Mostafa Portfolio API")

# CORS - Allow your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://www.mostafa-ai.cloud/"  # Add your production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Mostafa Portfolio API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
