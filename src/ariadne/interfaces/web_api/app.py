"""New product web API application."""

from __future__ import annotations

import uvicorn
import uuid
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from ariadne.interfaces.web_api.error_handlers import domain_error_handler, validation_error_handler
from ariadne.interfaces.web_api.routers import (
    annotations,
    dataset_versions,
    executions,
    graph_versions,
    projects,
    results,
    artifacts,
    exploration,
    predictive,
    predictive_workflow,
    workspace_lifecycle,
)
from ariadne.product.domain.errors import DomainError, InfrastructureError


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ariadne Product API",
        version="0.1.0",
        description="Causal discovery and inference platform – MVP API",
    )

    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(InfrastructureError, domain_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

    @app.middleware("http")
    async def request_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        request.state.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Request-Id"] = request.state.request_id
        return response

    for router in (projects.router, dataset_versions.router, executions.router, results.router,
                   graph_versions.router, annotations.router, artifacts.router,
                   exploration.router, predictive.router, workspace_lifecycle.router,
                   predictive_workflow.router):
        app.include_router(router, prefix="/api/v1")

    @app.get("/health/ready")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    uvicorn.run("ariadne.interfaces.web_api.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
