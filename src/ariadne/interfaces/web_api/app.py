"""New product web API application."""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from ariadne.interfaces.web_api.error_handlers import domain_error_handler
from ariadne.interfaces.web_api.routers import (
    annotations,
    dataset_versions,
    executions,
    graph_versions,
    projects,
    results,
)
from ariadne.product.domain.errors import DomainError


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ariadne Product API",
        version="0.1.0",
        description="Causal discovery and inference platform – MVP API",
    )

    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]

    app.include_router(projects.router)
    app.include_router(dataset_versions.router)
    app.include_router(executions.router)
    app.include_router(results.router)
    app.include_router(graph_versions.router)
    app.include_router(annotations.router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    uvicorn.run("ariadne.interfaces.web_api.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
