"""
app.py
------
Main FastAPI Application Entry Point.
Initializes:
    - Routers
    - CORS
    - JWT Auth
    - DB Connections
    - ML Models (GNN / anomaly / scoring)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.identity_router import router as identity_router
from routers.anomaly_router import router as anomaly_router
from routers.credibility_router import router as credibility_router
from routers.escrow_router import router as escrow_router
from routers.graph_router import router as graph_router
from routers.alerts_router import router as alerts_router
from routers.dashboard_router import router as dashboard_router
from routers.explainability_router import router as explainability_router


def create_app() -> FastAPI:
    app = FastAPI(title="FundWise Backend")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"]
    )

    # Register routers
    app.include_router(identity_router)
    app.include_router(anomaly_router)
    app.include_router(credibility_router)
    app.include_router(escrow_router)
    app.include_router(graph_router)
    app.include_router(alerts_router)
    app.include_router(dashboard_router)
    app.include_router(explainability_router)

    return app


app = create_app()

