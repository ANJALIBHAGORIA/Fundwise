from fastapi import FastAPI
# import routers (explicit imports for clarity)
from api.routers import identity_router, anomaly_router, credibility_router, escrow_router
from api.routers import graph_router, alerts_router, dashboard_router, explainability_router

app = FastAPI(title="FundWise API")

# include routers
app.include_router(identity_router.router)
app.include_router(anomaly_router.router)
app.include_router(credibility_router.router)
app.include_router(escrow_router.router)
app.include_router(graph_router.router)
app.include_router(alerts_router.router)
app.include_router(dashboard_router.router)
app.include_router(explainability_router.router)
