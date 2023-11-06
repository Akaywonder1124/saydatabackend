from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import database
from .routers import media

app = FastAPI()

# Define the list of allowed origins. "*" allows all origins; for production, specify the origin of your React app.
origins = ["*"]

# Configure CORS to allow requests from specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    await database.init()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.close()


app.include_router(media.router, prefix="/my-router", tags=["Upload"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
