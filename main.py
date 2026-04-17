from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="AI Security Autonomous Agent",
    version="1.0.0",
    description="Autonomous security agent for threat scoring, decisioning, and simulated response execution."
)

app.include_router(router)
