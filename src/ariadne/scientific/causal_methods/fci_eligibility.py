"""G01 P1-M06 exhaustive, pure pre-FCI eligibility."""
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from itertools import combinations, product
from math import comb, log1p, sqrt

import numpy as np
from scipy.special import erfc

from ariadne.causal.discovery.contracts import ValidatedDiscoveryRequest, exact_integer
from ariadne.scientific.capabilities import backend_error, unsupported

_EPSILON = np.finfo(np.float64).eps


@dataclass(frozen=True)
class EligibilityEvidence:
    ci_test: str
    columns: int
    rows: int
    expected_triples: int
    examined_triples: int
    minimum_expected_count: float | None


def _triples(p: int):
    for x, y in combinations(range(p), 2):
        remaining = tuple(i for i in range(p) if i != x and i != y)
        for size in range(p - 1):
            for conditioned in combinations(remaining, size):
                yield x, y, conditioned


def _numerical_block():
    return backend_error("ELIGIBILITY_UNRESOLVED", "Fisher Z numerical eligibility could not be verified")


def _fisherz(correlation, indices, n: int) -> None:
    degrees = n - len(indices) - 1
    if degrees <= 0:
        raise unsupported("Insufficient Fisher Z sample size")
    r_matrix = correlation[np.ix_(indices, indices)]
    if not np.isfinite(r_matrix).all():
        raise _numerical_block()
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            np.linalg.cholesky(r_matrix)
            condition = np.linalg.cond(r_matrix, p=2)
            if not np.isfinite(condition) or condition * _EPSILON > 1e-6:
                raise _numerical_block()
            inverse = np.linalg.inv(r_matrix)
            identity = np.eye(len(indices), dtype=np.float64)
            left = np.linalg.norm(r_matrix @ inverse - identity, ord=np.inf)
            right = np.linalg.norm(inverse @ r_matrix - identity, ord=np.inf)
            if not np.isfinite(inverse).all() or not np.isfinite([left, right]).all() or max(left, right) > 1e-8:
                raise _numerical_block()
            denominator = inverse[0, 0] * inverse[1, 1]
            if not np.isfinite(denominator) or denominator <= 0:
                raise _numerical_block()
            partial = -inverse[0, 1] / sqrt(denominator)
            if not np.isfinite(partial) or abs(partial) >= 1:
                raise _numerical_block()
            transform = 0.5 * (log1p(partial) - log1p(-partial))
            statistic = sqrt(degrees) * abs(transform)
            if not np.isfinite([transform, statistic, erfc(statistic / sqrt(2))]).all():
                raise _numerical_block()
    except (np.linalg.LinAlgError, FloatingPointError, OverflowError) as error:
        raise _numerical_block() from error


def _categorical(rows, domains, x: int, y: int, conditioned: tuple[int, ...],
                 check_resources: Callable[[], None]) -> float:
    strata = {}
    for row in rows:
        key = tuple(row[i] for i in conditioned)
        strata.setdefault(key, Counter())[row[x], row[y]] += 1
    minimum = float("inf")
    for key in product(*(domains[i] for i in conditioned)):
        check_resources()
        table = strata.get(key)
        if not table:
            raise unsupported("Declared conditioning category has no support")
        row_totals, column_totals = Counter(), Counter()
        for (x_code, y_code), count in table.items():
            row_totals[x_code] += count
            column_totals[y_code] += count
        total = sum(row_totals.values())
        for x_code, y_code in product(domains[x], domains[y]):
            product_count = row_totals[x_code] * column_totals[y_code]
            if product_count < 5 * total:
                raise unsupported("Declared contingency cell has expected support below five")
            minimum = min(minimum, product_count / total)
    return minimum


class ScientificEligibilityPolicy:
    """Run complete screening while an injected trusted resource check permits it."""

    def __init__(self, resources_available: Callable[[], bool]):
        self._resources_available = resources_available

    def _check_resources(self) -> None:
        if self._resources_available() is not True:
            raise backend_error("ELIGIBILITY_UNRESOLVED", "Exhaustive CI screening resources are unavailable")

    def check(self, request: ValidatedDiscoveryRequest) -> tuple[np.ndarray, EligibilityEvidence]:
        if type(request) is not ValidatedDiscoveryRequest:
            raise unsupported("Expected validated Discovery request")
        request.capability.check(request.capability_request)
        config = request.study.to_payload()["method"]["config"]
        if set(config) != {"indep_test", "alpha", "depth", "max_path_length", "background_knowledge"}:
            raise unsupported("Invalid FCI configuration shape")
        alpha = config["alpha"]
        if (type(alpha) not in (int, float) or not 0 < alpha < 1
            or any(type(config[name]) is not int or config[name] < -1 for name in ("depth", "max_path_length"))):
            raise unsupported("Invalid FCI alpha, depth or maximum path length")
        if config["background_knowledge"] is not None:
            raise backend_error("BACKEND_SEMANTICS_UNVERIFIED", "Non-null FCI background knowledge is unavailable")
        n, p = len(request.rows), len(request.columns)
        expected = comb(p, 2) * (1 << (p - 2))
        profile = request.capability.profile
        examined = 0
        minimum = None
        try:
            self._check_resources()
            if profile == "fisherz":
                data = np.asarray(request.rows, dtype=np.float64)
                if (not np.isfinite(data).all()) or np.any(np.max(data, axis=0) == np.min(data, axis=0)):
                    raise unsupported("Fisher Z requires finite nonconstant continuous columns")
                if n <= p + 1:
                    raise unsupported("Insufficient Fisher Z sample size for exhaustive conditioning")
                with np.errstate(over="raise", invalid="raise", divide="raise"):
                    correlation = np.corrcoef(data.T)
            else:
                domains = tuple(item.category_codes for item in request.capability_request.design.variables)
                membership = tuple(frozenset(codes) for codes in domains)
                for row in request.rows:
                    if any(not exact_integer(value) or value not in allowed for value, allowed in zip(row, membership)):
                        raise unsupported("Dataset integer code is outside its declared Design domain")
                data = np.asarray(request.rows, dtype=np.int64)
            for x, y, conditioned in _triples(p):
                self._check_resources()
                if profile == "fisherz":
                    _fisherz(correlation, [x, y, *conditioned], n)
                else:
                    observed = _categorical(request.rows, domains, x, y, conditioned, self._check_resources)
                    minimum = observed if minimum is None else min(minimum, observed)
                examined += 1
        except (MemoryError, TimeoutError, OverflowError, FloatingPointError) as error:
            raise backend_error("ELIGIBILITY_UNRESOLVED", "Exhaustive CI screening did not complete") from error
        if examined != expected:
            raise backend_error("ELIGIBILITY_UNRESOLVED", "Exhaustive CI evaluation did not complete")
        return data, EligibilityEvidence(profile, p, n, expected, examined, minimum)
