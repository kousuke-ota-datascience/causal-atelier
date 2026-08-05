"""明示的な treatment effect を推定する estimator 群。"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..constants import SUPPORTED_EFFECT_METHODS, SUPPORTED_ESTIMANDS, SUPPORTED_ROBUST_SE
from .inference import effective_sample_size, records_to_frame, weighted_mean, weighted_variance
from .linear_model import confidence_interval, fit_linear_regression, normal_p_value, numeric_matrix
from ..nuisance.propensity import fit_logistic_propensity, logistic


@dataclass(frozen=True)
class TreatmentEffectResult:
    """treatment effect 推定結果。

    Attributes:
        method: Estimation method name.
        estimand: Target estimand such as ``ATE`` or ``ATT``.
        treatment: Treatment column name.
        outcome: Outcome column name.
        adjustment_set: Covariates used for adjustment.
        n: Number of observations used for estimation.
        n_treated: Number of treated observations.
        n_control: Number of control observations.
        effect: Estimated treatment effect.
        std_error: Approximate standard error.
        ci_low: Lower confidence interval bound.
        ci_high: Upper confidence interval bound.
        p_value: Approximate p-value.
        notes: Method-specific notes and limitations.
    """

    method: str
    estimand: str
    treatment: str
    outcome: str
    adjustment_set: list[str]
    n: int
    n_treated: int
    n_control: int
    effect: float
    std_error: float | None
    ci_low: float | None
    ci_high: float | None
    p_value: float | None
    notes: str = ""


def validate_treatment_effect_inputs(
    frame: pd.DataFrame,
    treatment: str,
    outcome: str,
) -> None:
    """treatment effect 推定に必要な入力列を検証する。

    Args:
        frame: Analysis frame.
        treatment: Treatment column name.
        outcome: Outcome column name.

    Raises:
        ValueError: If treatment/outcome columns are missing or the treatment
            is not binary.
    """
    if treatment not in frame.columns:
        raise ValueError(f"treatment column is missing from frame: {treatment}")
    if outcome not in frame.columns:
        raise ValueError(f"outcome column is missing from frame: {outcome}")
    values = set(pd.to_numeric(frame[treatment].dropna(), errors="coerce").unique())
    if values.difference({0.0, 1.0}):
        raise ValueError(
            "Treatment must be binary for current estimators. "
            f"Observed values: {sorted(values)}"
        )


class TreatmentEffectEstimator:
    """指定された adjustment strategy のもとで treatment effect を推定する。

    The estimators identify ATE or ATT only under the usual adjustment
    assumptions: consistency, positivity/overlap, no unobserved confounding
    conditional on the selected covariates, and correct enough nuisance models
    for model-based estimators. These assumptions are not verified by code.

    Args:
        frame: Household-level analysis frame.
        treatment: Binary treatment column.
        outcome: Outcome column.
        covariates: Adjustment covariates.
        estimand: Target estimand. Supported values are ``ATE`` and ``ATT``.
        robust_se: Robust standard error type for OLS-based estimators.
        propensity_clip: Lower and upper bounds used to clip propensity scores.
        cross_fitting_folds: Number of folds for cross-fitting. ``0``
            preserves the legacy no-sample-splitting behavior.
    """

    def __init__(
        self,
        frame: pd.DataFrame,
        treatment: str,
        outcome: str,
        covariates: list[str],
        estimand: str = "ATE",
        robust_se: str = "HC3",
        propensity_clip: tuple[float, float] = (0.01, 0.99),
        cross_fitting_folds: int = 0,
    ) -> None:
        """estimator を初期化する。

        Args:
            frame: Household-level analysis frame.
            treatment: Binary treatment column.
            outcome: Outcome column.
            covariates: Adjustment covariates.
            estimand: Target estimand.
            robust_se: Robust standard error type.
            propensity_clip: Lower and upper propensity clipping bounds.
            cross_fitting_folds: Number of folds for cross-fitting.

        Raises:
            ValueError: If estimand, robust SE, clip bounds, or inputs are
                invalid.
        """
        if estimand not in SUPPORTED_ESTIMANDS:
            raise ValueError(f"estimand must be ATE or ATT: {estimand}")
        if robust_se not in SUPPORTED_ROBUST_SE:
            raise ValueError(f"robust_se must be one of {SUPPORTED_ROBUST_SE}: {robust_se}")
        if not 0 < propensity_clip[0] < propensity_clip[1] < 1:
            raise ValueError("propensity_clip must satisfy 0 < lower < upper < 1")
        validate_treatment_effect_inputs(frame, treatment, outcome)
        self.frame = frame
        self.treatment = treatment
        self.outcome = outcome
        self.covariates = covariates
        self.estimand = estimand
        self.robust_se = robust_se
        self.propensity_clip = propensity_clip
        self.cross_fitting_folds = cross_fitting_folds
        self.last_propensity_score: np.ndarray | None = None
        self.last_propensity_notes = ""

    def complete_case_data(self, include_covariates: bool) -> pd.DataFrame:
        """指定 estimator が使う complete-case data を返す。

        Args:
            include_covariates: Whether covariates must be complete.

        Returns:
            Complete-case data frame.
        """
        columns = [self.treatment, self.outcome]
        if include_covariates:
            columns.extend(self.covariates)
        return self.frame.loc[:, columns].dropna()

    def result(
        self,
        *,
        method: str,
        data: pd.DataFrame,
        effect: float,
        std_error: float | None,
        notes: str,
        estimand: str | None = None,
    ) -> TreatmentEffectResult:
        """標準化された treatment-effect result object を作る。

        Args:
            method: Estimation method name.
            data: Data used by the estimator.
            effect: Point estimate.
            std_error: Approximate standard error.
            notes: Method-specific notes.

        Returns:
            Treatment-effect result with confidence interval and p-value.
        """
        t = data[self.treatment].astype(float)
        ci_low, ci_high = confidence_interval(effect, std_error)
        p_value = (
            normal_p_value(effect / std_error)
            if std_error is not None and std_error > 0
            else None
        )
        return TreatmentEffectResult(
            method=method,
            estimand=self.estimand if estimand is None else estimand,
            treatment=self.treatment,
            outcome=self.outcome,
            adjustment_set=list(self.covariates),
            n=int(len(data)),
            n_treated=int((t == 1.0).sum()),
            n_control=int((t == 0.0).sum()),
            effect=float(effect),
            std_error=float(std_error) if std_error is not None else None,
            ci_low=ci_low,
            ci_high=ci_high,
            p_value=p_value,
            notes=notes,
        )

    def estimate(self, methods: list[str]) -> pd.DataFrame:
        """指定された method 群で treatment effect を推定する。

        Args:
            methods: Method names to run.

        Returns:
            Treatment-effect result table.

        Raises:
            ValueError: If an unknown method is requested.
        """
        records = []
        runners = {
            "diff_in_means": self.diff_in_means,
            "ols_coefficient": self.ols,
            "g_computation_ate": lambda: self.g_computation("ATE"),
            "g_computation_att": lambda: self.g_computation("ATT"),
            "ipw_ate": lambda: self.ipw("ATE"),
            "ipw_att": lambda: self.ipw("ATT"),
            "aipw_ate": lambda: self.aipw("ATE"),
            "aipw_att": lambda: self.aipw("ATT"),
        }
        for method in methods:
            if method not in SUPPORTED_EFFECT_METHODS:
                raise ValueError(f"unknown effect method: {method}")
            if method.endswith("_ate") and self.estimand != "ATE":
                raise ValueError(f"{method} is unsupported when estimand={self.estimand}")
            if method.endswith("_att") and self.estimand != "ATT":
                raise ValueError(f"{method} is unsupported when estimand={self.estimand}")
            records.append(runners[method]().__dict__)
        columns = list(TreatmentEffectResult.__dataclass_fields__.keys())
        return records_to_frame(records, columns)

    def diff_in_means(self) -> TreatmentEffectResult:
        """未調整の treated-control mean difference を推定する。

        Returns:
            Treatment-effect result. The numerical contrast is identical for
            ATE and ATT, but it is not adjusted for confounding.
        """
        data = self.complete_case_data(include_covariates=False)
        y = data[self.outcome].to_numpy(dtype=float)
        t = data[self.treatment].to_numpy(dtype=float)
        y_treated = y[t == 1.0]
        y_control = y[t == 0.0]
        if len(y_treated) == 0 or len(y_control) == 0:
            raise ValueError("diff_in_means requires both treated and control observations")
        effect = float(y_treated.mean() - y_control.mean())
        variance_treated = float(np.var(y_treated, ddof=1)) if len(y_treated) > 1 else 0.0
        variance_control = float(np.var(y_control, ddof=1)) if len(y_control) > 1 else 0.0
        standard_error = math.sqrt(
            variance_treated / len(y_treated) + variance_control / len(y_control)
        )
        return self.result(
            method="diff_in_means",
            data=data,
            effect=effect,
            std_error=standard_error,
            notes="unadjusted_difference; numerical contrast is identical for ATE and ATT",
        )

    def ols(self) -> TreatmentEffectResult:
        """回帰調整済み treatment coefficient を推定する。

        Returns:
            Treatment-effect result using the treatment coefficient from
            ``outcome ~ treatment + covariates``.
        """
        data = self.complete_case_data(include_covariates=True)
        y = data[self.outcome].to_numpy(dtype=float)
        regressors = [self.treatment, *self.covariates]
        x = numeric_matrix(data, regressors)
        fit = fit_linear_regression(y, x, robust_se=self.robust_se)
        effect = float(fit.coefficients[1])
        standard_error = float(fit.standard_errors[1])
        notes = [
            f"robust_se={self.robust_se}",
            f"rank={fit.rank}/{x.shape[1] + 1}",
            f"condition_number={fit.condition_number:.6g}",
            "normal_approximation_for_ci_and_p_value",
        ]
        if fit.rank < x.shape[1] + 1:
            notes.append("rank_deficient_design_pinv_used")
        return self.result(
            method="ols_coefficient",
            data=data,
            effect=effect,
            std_error=standard_error,
            estimand="regression_coefficient",
            notes="; ".join(notes),
        )

    def g_computation(self, estimand: str) -> TreatmentEffectResult:
        """Estimate ATE or ATT by regression g-computation."""

        data = self.complete_case_data(include_covariates=True)
        y = data[self.outcome].to_numpy(dtype=float)
        t = data[self.treatment].to_numpy(dtype=float)
        regressors = [self.treatment, *self.covariates]
        x = numeric_matrix(data, regressors)
        fit = fit_linear_regression(y, x, robust_se=self.robust_se)

        observed_covariates = numeric_matrix(data, self.covariates)
        treated_design = np.column_stack(
            [np.ones(len(data)), np.ones(len(data)), observed_covariates]
        )
        control_design = np.column_stack(
            [np.ones(len(data)), np.zeros(len(data)), observed_covariates]
        )
        individual_effect = treated_design @ fit.coefficients - control_design @ fit.coefficients
        if estimand == "ATE":
            target_effect = individual_effect
        elif estimand == "ATT":
            target_effect = individual_effect[t == 1.0]
        else:
            raise ValueError(f"unsupported g-computation estimand: {estimand}")
        if len(target_effect) == 0:
            raise ValueError(f"g-computation {estimand} requires non-empty target population")
        effect = float(np.mean(target_effect))
        standard_error = float(np.std(target_effect, ddof=1) / math.sqrt(len(target_effect))) if len(target_effect) > 1 else 0.0
        return self.result(
            method=f"g_computation_{estimand.lower()}",
            data=data,
            effect=effect,
            std_error=standard_error,
            estimand=estimand,
            notes=(
                f"linear_outcome_model; robust_se={self.robust_se}; "
                "standard_error_from_empirical_individual_effects"
            ),
        )

    def propensity_data(self) -> tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]:
        """propensity score を推定し、complete-case array 群を返す。

        Returns:
            Tuple of data frame, outcome array, treatment array, and clipped
            propensity scores.
        """
        data = self.complete_case_data(include_covariates=True)
        y = data[self.outcome].to_numpy(dtype=float)
        t = data[self.treatment].to_numpy(dtype=float)
        x = numeric_matrix(data, self.covariates)
        propensity_raw, notes = fit_logistic_propensity(t, x)
        propensity_score = np.clip(propensity_raw, *self.propensity_clip)
        self.last_propensity_score = propensity_raw
        self.last_propensity_notes = notes
        return data, y, t, propensity_score

    def ipw(self, estimand: str) -> TreatmentEffectResult:
        """inverse-probability-weighted effect を推定する。

        Returns:
            Treatment-effect result using a logistic propensity model and
            configured propensity clipping.
        """
        data, y, t, propensity_score = self.propensity_data()
        if estimand == "ATE":
            weights_treated = t / propensity_score
            weights_control = (1.0 - t) / (1.0 - propensity_score)
        elif estimand == "ATT":
            weights_treated = t
            weights_control = (1.0 - t) * propensity_score / (1.0 - propensity_score)
        else:
            raise ValueError(f"unsupported IPW estimand: {estimand}")

        mean_treated = weighted_mean(y, weights_treated)
        mean_control = weighted_mean(y, weights_control)
        effect = float(mean_treated - mean_control)
        ess_treated = effective_sample_size(weights_treated)
        ess_control = effective_sample_size(weights_control)
        variance_treated = weighted_variance(y, weights_treated, mean_treated)
        variance_control = weighted_variance(y, weights_control, mean_control)
        standard_error = math.sqrt(
            variance_treated / ess_treated + variance_control / ess_control
        )
        raw = self.last_propensity_score
        lower, upper = self.propensity_clip
        overlap_warning = ""
        if raw is not None and ((raw < lower).any() or (raw > upper).any()):
            overlap_warning = f"; overlap_warning=propensity_outside_[{lower},{upper}]"
        notes = (
            f"propensity_logit; stabilized_normalized_weights; clip=[{lower},{upper}]; "
            f"ess_treated={ess_treated:.6g}; ess_control={ess_control:.6g}"
            f"{overlap_warning}"
        )
        if self.last_propensity_notes:
            notes = f"{notes}; {self.last_propensity_notes}"
        return self.result(
            method=f"ipw_{estimand.lower()}",
            data=data,
            effect=effect,
            std_error=standard_error,
            estimand=estimand,
            notes=notes,
        )

    def aipw(self, estimand: str) -> TreatmentEffectResult:
        """augmented inverse-probability-weighted effect を推定する。

        Returns:
            Treatment-effect result. Cross-fitting is not yet implemented; a
            nonzero ``cross_fitting_folds`` value is recorded in notes only.
        """
        data, y, t, propensity_score = self.propensity_data()
        x = numeric_matrix(data, self.covariates)
        treated_mask = t == 1.0
        control_mask = t == 0.0
        if treated_mask.sum() <= x.shape[1] + 1 or control_mask.sum() <= x.shape[1] + 1:
            return self.result(
                method="aipw",
                data=data,
                effect=np.nan,
                std_error=None,
                notes="skipped_insufficient_sample_size_for_outcome_models",
            )

        if self.cross_fitting_folds > 1:
            propensity_score, mu_treated, mu_control, nuisance_notes = self.cross_fitted_nuisance(
                y,
                t,
                x,
            )
        else:
            treated_fit = fit_linear_regression(y[treated_mask], x[treated_mask])
            control_fit = fit_linear_regression(y[control_mask], x[control_mask])
            design = np.column_stack([np.ones(len(data)), x])
            mu_treated = design @ treated_fit.coefficients
            mu_control = design @ control_fit.coefficients
            nuisance_notes = "no_sample_splitting"

        if estimand == "ATE":
            score = (
                mu_treated
                - mu_control
                + t / propensity_score * (y - mu_treated)
                - (1.0 - t) / (1.0 - propensity_score) * (y - mu_control)
            )
        elif estimand == "ATT":
            treated_rate = float(t.mean())
            score = (
                t / treated_rate * (y - mu_control)
                - (1.0 - t)
                * propensity_score
                / (1.0 - propensity_score)
                / treated_rate
                * (y - mu_control)
            )
        else:
            raise ValueError(f"unsupported AIPW estimand: {estimand}")
        effect = float(score.mean())
        standard_error = float(np.std(score, ddof=1) / math.sqrt(len(score)))
        lower, upper = self.propensity_clip
        notes = (
            f"aipw_linear_outcome_models; propensity_logit; clip=[{lower},{upper}]; "
            f"{nuisance_notes}; cross_fitting_folds={self.cross_fitting_folds}"
        )
        if self.last_propensity_notes:
            notes = f"{notes}; {self.last_propensity_notes}"
        return self.result(
            method=f"aipw_{estimand.lower()}",
            data=data,
            effect=effect,
            std_error=standard_error,
            estimand=estimand,
            notes=notes,
        )

    def cross_fitted_nuisance(
        self,
        y: np.ndarray,
        t: np.ndarray,
        x: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
        """Fit propensity and outcome nuisance models with deterministic folds."""

        folds = min(self.cross_fitting_folds, len(y))
        if folds < 2:
            raise ValueError("cross_fitting_folds must be at least 2 for cross-fitting")
        fold_ids = _stratified_fold_ids(t, folds)
        propensity_score = np.empty(len(y), dtype=float)
        mu_treated = np.empty(len(y), dtype=float)
        mu_control = np.empty(len(y), dtype=float)
        notes: list[str] = []
        for fold in range(folds):
            test_mask = fold_ids == fold
            train_mask = ~test_mask
            if (t[train_mask] == 1.0).sum() == 0 or (t[train_mask] == 0.0).sum() == 0:
                raise ValueError("AIPW cross-fitting requires treated and control observations in every training fold")
            propensity_score[test_mask], propensity_note = _fit_logistic_propensity_predict(
                t[train_mask],
                x[train_mask],
                x[test_mask],
            )
            if propensity_note:
                notes.append(f"fold_{fold}:{propensity_note}")
            treated_fit = fit_linear_regression(
                y[train_mask & (t == 1.0)],
                x[train_mask & (t == 1.0)],
            )
            control_fit = fit_linear_regression(
                y[train_mask & (t == 0.0)],
                x[train_mask & (t == 0.0)],
            )
            test_design = np.column_stack([np.ones(test_mask.sum()), x[test_mask]])
            mu_treated[test_mask] = test_design @ treated_fit.coefficients
            mu_control[test_mask] = test_design @ control_fit.coefficients
        clipped = np.clip(propensity_score, *self.propensity_clip)
        self.last_propensity_score = propensity_score
        return clipped, mu_treated, mu_control, "cross_fitted_nuisance_models" + (
            f"; {'; '.join(notes)}" if notes else ""
        )


def _fit_logistic_propensity_predict(
    treatment: np.ndarray,
    train_covariates: np.ndarray,
    test_covariates: np.ndarray,
    *,
    max_iter: int = 100,
    tol: float = 1e-8,
    ridge: float = 1e-6,
) -> tuple[np.ndarray, str]:
    """Fit a ridge logistic model on train rows and predict test rows."""

    x_train = np.column_stack([np.ones(len(treatment)), train_covariates])
    x_test = np.column_stack([np.ones(len(test_covariates)), test_covariates])
    beta = np.zeros(x_train.shape[1], dtype=float)
    converged = False
    for _ in range(max_iter):
        probability = logistic(x_train @ beta)
        weights = np.clip(probability * (1.0 - probability), 1e-8, None)
        hessian = x_train.T @ (weights[:, None] * x_train)
        penalty = np.eye(x_train.shape[1]) * ridge
        penalty[0, 0] = 0.0
        score = x_train.T @ (treatment - probability) - penalty @ beta
        try:
            delta = np.linalg.solve(hessian + penalty, score)
        except np.linalg.LinAlgError:
            delta = np.linalg.pinv(hessian + penalty) @ score
        beta = beta + delta
        if float(np.max(np.abs(delta))) < tol:
            converged = True
            break
    notes = "" if converged else "propensity_logit_not_converged"
    return logistic(x_test @ beta), notes


def _stratified_fold_ids(treatment: np.ndarray, folds: int) -> np.ndarray:
    """Assign deterministic folds within treatment strata."""

    fold_ids = np.empty(len(treatment), dtype=int)
    for treatment_value in (0.0, 1.0):
        indices = np.flatnonzero(treatment == treatment_value)
        if len(indices) < folds:
            raise ValueError(
                "AIPW cross-fitting requires each treatment group to have at least as many observations as folds"
            )
        for offset, index in enumerate(indices):
            fold_ids[index] = offset % folds
    return fold_ids
