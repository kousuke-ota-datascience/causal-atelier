from __future__ import annotations

import pytest

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.web_api import dependencies
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.domain.errors import OperationAvailabilityError
from ariadne.product.persistence.orm_models import ProjectMembershipOrm, ProjectOrm


def _service(product_env) -> ProductClosureService:  # type: ignore[no-untyped-def]
    _, root = product_env
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(ProjectOrm(project_id="p1", name="P1", status="ACTIVE"))
        session.flush()
        session.add(ProjectMembershipOrm(
            membership_id="membership-1", project_id="p1", user_id="owner",
            role="OWNER",
        ))
        session.commit()
    return ProductClosureService(factory, LocalArtifactStore(root / "objects"))


def test_operation_availability_accepts_a_valid_canonical_route(product_env) -> None:  # type: ignore[no-untyped-def]
    service = _service(product_env)
    response = service.operation_availability(
        "p1", user_id="owner", resource_type=None, resource_id=None,
        route="/projects/p1/analysis/causal/setup",
    )
    assert response["operations"]["RUN"]["reason_code"] == "RESOURCE_REQUIRED"


@pytest.mark.parametrize("route", [
    "/projects/p1/analysis/causal/unknown-stage",
    "/projects/p1/analysis/unknown/setup",
    "/projects/p1/analysis/causal",
    "/projects/p1/analysis/causal/setup/resource/unknown/id1",
    "/projects/p2/analysis/causal/setup",
])
def test_operation_availability_rejects_noncanonical_routes_before_projection(product_env, route: str) -> None:  # type: ignore[no-untyped-def]
    service = _service(product_env)
    with pytest.raises(OperationAvailabilityError) as caught:
        service.operation_availability(
            "p1", user_id="owner", resource_type=None, resource_id=None, route=route,
        )
    assert caught.value.code == "INVALID_NAVIGATION_ROUTE"
    assert caught.value.status == 422
