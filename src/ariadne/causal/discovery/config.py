from __future__ import annotations

import argparse
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Mapping

from ariadne.infrastructure.config import (
    ensure_mapping as _as_mapping,
    load_yaml_mapping,
    resolve_project_path as _resolve_project_path,
    write_yaml_snapshots,
)

from .constants import (
    ALLOWED_ALGORITHMS,
    DEFAULT_ALPHA_GRID,
    DEFAULT_DATASET_YAML,
    DEFAULT_DISCRETE_PC_INDEP_TESTS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PC_INDEP_TESTS,
)
from ariadne.preprocessing.discovery.config import FeatureConfig


def _as_bool(value: Any, field_name: str) -> bool:
    """YAML 値が boolean であることを検証する。

    Args:
        value: Parsed YAML value.
        field_name: Human-readable field name for error messages.

    Returns:
        ``value`` typed as ``bool``.

    Raises:
        ValueError: If ``value`` is not a boolean.
    """
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")
    return value


@dataclass(frozen=True)
class DatasetConfig:
    """``analysis.yaml`` の dataset registry 設定。

    Attributes:
        yaml_path: Dataset registry YAML path.
    """

    yaml_path: Path = DEFAULT_DATASET_YAML

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "DatasetConfig":
        """Build dataset configuration from YAML data.

        Args:
            value: Mapping under the ``dataset`` key.

        Returns:
            Parsed dataset configuration.
        """
        data = _as_mapping(value or {}, "dataset")
        return cls(yaml_path=Path(data.get("yaml_path", cls.yaml_path)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the dataset configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"yaml_path": str(self.yaml_path)}


@dataclass(frozen=True)
class RunConfig:
    """``analysis.yaml`` の runtime 設定。

    Attributes:
        campaign_id: Campaign identifier to analyze.
        pre_weeks: Number of pre-treatment weeks.
        output_dir: Directory where outputs are written.
        random_seed: Random seed for stochastic diagnostics.
    """

    campaign_id: str = "18"
    pre_weeks: int = 8
    output_dir: Path = DEFAULT_OUTPUT_DIR
    random_seed: int = 20260630

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "RunConfig":
        """Build runtime configuration from YAML data.

        Args:
            value: Mapping under the ``run`` key.

        Returns:
            Parsed runtime configuration.

        Raises:
            ValueError: If ``pre_weeks`` is not positive.
        """
        data = _as_mapping(value or {}, "run")
        pre_weeks = int(data.get("pre_weeks", cls.pre_weeks))
        if pre_weeks < 1:
            raise ValueError("run.pre_weeks must be positive")
        return cls(
            campaign_id=str(data.get("campaign_id", cls.campaign_id)),
            pre_weeks=pre_weeks,
            output_dir=Path(data.get("output_dir", cls.output_dir)),
            random_seed=int(data.get("random_seed", cls.random_seed)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize runtime configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {
            "campaign_id": self.campaign_id,
            "pre_weeks": self.pre_weeks,
            "output_dir": str(self.output_dir),
            "random_seed": self.random_seed,
        }


@dataclass(frozen=True)
class PreprocessingConfig:
    """``analysis.yaml`` の preprocessing 設定。

    Attributes:
        collinearity_threshold: Maximum allowed absolute pairwise correlation.
    """

    collinearity_threshold: float = 0.995

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "PreprocessingConfig":
        """Build preprocessing configuration from YAML data.

        Args:
            value: Mapping under the ``preprocessing`` key.

        Returns:
            Parsed preprocessing configuration.

        Raises:
            ValueError: If ``collinearity_threshold`` is outside ``(0, 1]``.
        """
        data = _as_mapping(value or {}, "preprocessing")
        threshold = float(data.get("collinearity_threshold", cls.collinearity_threshold))
        if not 0 < threshold <= 1:
            raise ValueError("preprocessing.collinearity_threshold must be in (0, 1]")
        return cls(collinearity_threshold=threshold)

    def to_dict(self) -> dict[str, Any]:
        """Serialize preprocessing configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"collinearity_threshold": self.collinearity_threshold}


@dataclass(frozen=True)
class PCConfig:
    """``analysis.yaml`` の PC algorithm 設定。

    Attributes:
        alpha: Main PC significance level.
        indep_test: Conditional-independence test name.
        allowed_indep_tests: Test names accepted by the CLI and schema.
        discrete_indep_tests: Test names that require discretization.
        discrete_bins: Number of quantile bins for discrete tests.
        alpha_grid: Alpha values for sensitivity analysis.
    """

    alpha: float = 0.01
    indep_test: str = "fisherz"
    allowed_indep_tests: tuple[str, ...] = DEFAULT_PC_INDEP_TESTS
    discrete_indep_tests: tuple[str, ...] = DEFAULT_DISCRETE_PC_INDEP_TESTS
    discrete_bins: int = 4
    alpha_grid: tuple[float, ...] = DEFAULT_ALPHA_GRID

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "PCConfig":
        """Build PC configuration from YAML data.

        Args:
            value: Mapping under ``discovery.pc``.

        Returns:
            Parsed PC configuration.

        Raises:
            ValueError: If tests, bins, or alpha grid are invalid.
        """
        data = _as_mapping(value or {}, "discovery.pc")
        allowed = tuple(str(item) for item in data.get("allowed_indep_tests", cls.allowed_indep_tests))
        discrete = tuple(str(item) for item in data.get("discrete_indep_tests", cls.discrete_indep_tests))
        indep_test = str(data.get("indep_test", cls.indep_test))
        discrete_bins = int(data.get("discrete_bins", cls.discrete_bins))
        alpha_grid = tuple(float(item) for item in data.get("alpha_grid", cls.alpha_grid))

        if indep_test not in allowed:
            raise ValueError("discovery.pc.indep_test must be in allowed_indep_tests")
        if not set(discrete).issubset(set(allowed)):
            raise ValueError("discovery.pc.discrete_indep_tests must be a subset of allowed_indep_tests")
        if discrete_bins < 2:
            raise ValueError("discovery.pc.discrete_bins must be at least 2")
        if not alpha_grid:
            raise ValueError("discovery.pc.alpha_grid must not be empty")

        return cls(
            alpha=float(data.get("alpha", cls.alpha)),
            indep_test=indep_test,
            allowed_indep_tests=allowed,
            discrete_indep_tests=discrete,
            discrete_bins=discrete_bins,
            alpha_grid=alpha_grid,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize PC configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {
            "alpha": self.alpha,
            "indep_test": self.indep_test,
            "allowed_indep_tests": list(self.allowed_indep_tests),
            "discrete_indep_tests": list(self.discrete_indep_tests),
            "discrete_bins": self.discrete_bins,
            "alpha_grid": list(self.alpha_grid),
        }


@dataclass(frozen=True)
class NotearsConfig:
    """``analysis.yaml`` の NOTEARS 設定。

    Attributes:
        threshold: Absolute edge-weight threshold for reporting.
    """

    threshold: float = 0.3

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "NotearsConfig":
        """Build NOTEARS configuration from YAML data.

        Args:
            value: Mapping under ``discovery.notears``.

        Returns:
            Parsed NOTEARS configuration.
        """
        data = _as_mapping(value or {}, "discovery.notears")
        return cls(threshold=float(data.get("threshold", cls.threshold)))

    def to_dict(self) -> dict[str, Any]:
        """Serialize NOTEARS configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"threshold": self.threshold}


@dataclass(frozen=True)
class GESConfig:
    """``analysis.yaml`` の GES 設定。

    Attributes:
        maxP: Maximum number of parents for each node (None = unlimited).
        score_func: Score function name.
    """

    maxP: int | None = None
    score_func: str = "local_score_BIC"

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "GESConfig":
        """Build GES configuration from YAML data.

        Args:
            value: Mapping under ``discovery.ges``.

        Returns:
            Parsed GES configuration.
        """
        data = _as_mapping(value or {}, "discovery.ges")
        max_p = data.get("maxP", cls.maxP)
        return cls(
            maxP=int(max_p) if max_p is not None else None,
            score_func=str(data.get("score_func", cls.score_func)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize GES configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"maxP": self.maxP, "score_func": self.score_func}


@dataclass(frozen=True)
class DiscoveryConfig:
    """``analysis.yaml`` の因果探索アルゴリズム設定。

    Attributes:
        algorithms: Algorithm names to run.
        use_background_knowledge: Whether to apply configured temporal tiers.
        pc: PC-specific settings.
        ges: GES-specific settings.
        notears: NOTEARS-specific settings.
    """

    algorithms: tuple[str, ...] = ALLOWED_ALGORITHMS
    use_background_knowledge: bool = True
    pc: PCConfig = field(default_factory=PCConfig)
    ges: GESConfig = field(default_factory=GESConfig)
    notears: NotearsConfig = field(default_factory=NotearsConfig)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "DiscoveryConfig":
        """Build discovery configuration from YAML data.

        Args:
            value: Mapping under the ``discovery`` key.

        Returns:
            Parsed discovery configuration.

        Raises:
            ValueError: If no algorithm is selected or an algorithm is unknown.
        """
        data = _as_mapping(value or {}, "discovery")
        algorithms = tuple(str(item) for item in data.get("algorithms", cls.algorithms))
        unknown = set(algorithms).difference(ALLOWED_ALGORITHMS)
        if unknown:
            raise ValueError(f"discovery.algorithms contains unsupported values: {sorted(unknown)}")
        if not algorithms:
            raise ValueError("discovery.algorithms must not be empty")
        return cls(
            algorithms=algorithms,
            use_background_knowledge=_as_bool(
                data.get("use_background_knowledge", cls.use_background_knowledge),
                "discovery.use_background_knowledge",
            ),
            pc=PCConfig.from_mapping(data.get("pc")),
            ges=GESConfig.from_mapping(data.get("ges")),
            notears=NotearsConfig.from_mapping(data.get("notears")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize discovery configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {
            "algorithms": list(self.algorithms),
            "use_background_knowledge": self.use_background_knowledge,
            "pc": self.pc.to_dict(),
            "ges": self.ges.to_dict(),
            "notears": self.notears.to_dict(),
        }


@dataclass(frozen=True)
class BootstrapConfig:
    """``analysis.yaml`` の bootstrap diagnostic 設定。

    Attributes:
        samples: Number of bootstrap samples.
        sample_fraction: Fraction of rows sampled per bootstrap.
    """

    samples: int = 100
    sample_fraction: float = 1.0

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "BootstrapConfig":
        """Build bootstrap configuration from YAML data.

        Args:
            value: Mapping under ``diagnostics.bootstrap``.

        Returns:
            Parsed bootstrap configuration.

        Raises:
            ValueError: If sample count or fraction is invalid.
        """
        data = _as_mapping(value or {}, "diagnostics.bootstrap")
        samples = int(data.get("samples", cls.samples))
        sample_fraction = float(data.get("sample_fraction", cls.sample_fraction))
        if samples < 0:
            raise ValueError("diagnostics.bootstrap.samples must be non-negative")
        if not 0 < sample_fraction <= 1:
            raise ValueError("diagnostics.bootstrap.sample_fraction must be in (0, 1]")
        return cls(samples=samples, sample_fraction=sample_fraction)

    def to_dict(self) -> dict[str, Any]:
        """Serialize bootstrap configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"samples": self.samples, "sample_fraction": self.sample_fraction}


@dataclass(frozen=True)
class DiagnosticsConfig:
    """``analysis.yaml`` の diagnostic 設定。

    Attributes:
        bootstrap: Bootstrap edge-stability settings.
    """

    bootstrap: BootstrapConfig = field(default_factory=BootstrapConfig)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "DiagnosticsConfig":
        """Build diagnostics configuration from YAML data.

        Args:
            value: Mapping under the ``diagnostics`` key.

        Returns:
            Parsed diagnostics configuration.
        """
        data = _as_mapping(value or {}, "diagnostics")
        return cls(bootstrap=BootstrapConfig.from_mapping(data.get("bootstrap")))

    def to_dict(self) -> dict[str, Any]:
        """Serialize diagnostics configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {"bootstrap": self.bootstrap.to_dict()}


@dataclass(frozen=True)
class ReportingConfig:
    """``analysis.yaml`` の出力 switch 設定。

    Attributes:
        write_raw_input: Whether to write raw discovery input.
        write_processed_input: Whether to write transformed discovery input.
        write_standardized_input: Whether to write standardized input.
        write_variable_metadata: Whether to write variable metadata.
        write_variable_diagnostics: Whether to write variable diagnostics.
        write_algorithm_summary: Whether to write algorithm summary.
        write_graph_markdown: Whether to write graph Markdown reports.
        write_alpha_sensitivity: Whether to write PC alpha sensitivity outputs.
        write_bootstrap_stability: Whether to write bootstrap stability outputs.
    """

    write_raw_input: bool = True
    write_processed_input: bool = True
    write_standardized_input: bool = True
    write_variable_metadata: bool = True
    write_variable_diagnostics: bool = True
    write_algorithm_summary: bool = True
    write_graph_markdown: bool = True
    write_alpha_sensitivity: bool = True
    write_bootstrap_stability: bool = True

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "ReportingConfig":
        """Build reporting configuration from YAML data.

        Args:
            value: Mapping under the ``reporting`` key.

        Returns:
            Parsed reporting configuration.
        """
        data = _as_mapping(value or {}, "reporting")
        kwargs = {
            field_name: _as_bool(data.get(field_name, getattr(cls, field_name)), f"reporting.{field_name}")
            for field_name in cls.__dataclass_fields__
        }
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Serialize reporting configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {field_name: getattr(self, field_name) for field_name in self.__dataclass_fields__}


@dataclass(frozen=True)
class AnalysisConfig:
    """analysis 設定の top-level object。

    Attributes:
        dataset: Dataset registry settings.
        run: Runtime settings.
        preprocessing: Preprocessing settings.
        discovery: Discovery algorithm settings.
        diagnostics: Diagnostic settings.
        reporting: Output switches.
    """

    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    run: RunConfig = field(default_factory=RunConfig)
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    diagnostics: DiagnosticsConfig = field(default_factory=DiagnosticsConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AnalysisConfig":
        """Build top-level analysis configuration from YAML data.

        Args:
            value: Parsed ``analysis.yaml`` mapping.

        Returns:
            Validated analysis configuration.
        """
        data = _as_mapping(value, "analysis config")
        return cls(
            dataset=DatasetConfig.from_mapping(data.get("dataset")),
            run=RunConfig.from_mapping(data.get("run")),
            preprocessing=PreprocessingConfig.from_mapping(data.get("preprocessing")),
            discovery=DiscoveryConfig.from_mapping(data.get("discovery")),
            diagnostics=DiagnosticsConfig.from_mapping(data.get("diagnostics")),
            reporting=ReportingConfig.from_mapping(data.get("reporting")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize analysis configuration to YAML-compatible data.

        Returns:
            Dictionary representation.
        """
        return {
            "dataset": self.dataset.to_dict(),
            "run": self.run.to_dict(),
            "preprocessing": self.preprocessing.to_dict(),
            "discovery": self.discovery.to_dict(),
            "diagnostics": self.diagnostics.to_dict(),
            "reporting": self.reporting.to_dict(),
        }



def load_yaml(path: Path) -> dict[str, Any]:
    """YAML ファイルを辞書として読み込む。

    Args:
        path: YAML ファイルパス。

    Returns:
        parsing 済み YAML mapping。空ファイルは空辞書になる。

    Raises:
        ValueError: YAML root が mapping でない場合。
    """
    return load_yaml_mapping(path)


def load_analysis_config(path: Path) -> AnalysisConfig:
    """analysis 設定ファイルを読み込み validation する。

    Args:
        path: Path to ``analysis.yaml``.

    Returns:
        Validated analysis configuration.
    """
    return AnalysisConfig.from_mapping(load_yaml(path))


def resolve_project_path(path: Path, project_root: Path) -> Path:
    """project root から相対パスを解決する。"""
    return _resolve_project_path(path, project_root)


def merge_cli_overrides(
    analysis_config: AnalysisConfig,
    args: argparse.Namespace,
) -> AnalysisConfig:
    """CLI 引数による上書きを analysis 設定へ適用する。

    Args:
        analysis_config: Base configuration loaded from YAML.
        args: Parsed command-line namespace. ``None`` values are ignored.

    Returns:
        New validated configuration after applying overrides.

    Raises:
        ValueError: If the resulting configuration violates schema rules.
    """
    dataset = analysis_config.dataset
    run = analysis_config.run
    preprocessing = analysis_config.preprocessing
    discovery = analysis_config.discovery
    diagnostics = analysis_config.diagnostics
    pc = discovery.pc
    notears = discovery.notears
    bootstrap = diagnostics.bootstrap

    if args.dataset_yaml is not None:
        dataset = DatasetConfig(yaml_path=args.dataset_yaml)

    if args.campaign_id is not None:
        run = replace(run, campaign_id=str(args.campaign_id))
    if args.pre_weeks is not None:
        run = replace(run, pre_weeks=int(args.pre_weeks))
    if args.output_dir is not None:
        run = replace(run, output_dir=args.output_dir)
    if args.random_seed is not None:
        run = replace(run, random_seed=int(args.random_seed))

    if args.collinearity_threshold is not None:
        preprocessing = PreprocessingConfig(
            collinearity_threshold=float(args.collinearity_threshold)
        )

    if args.algorithms is not None:
        discovery = replace(discovery, algorithms=tuple(args.algorithms))
    if args.no_background_knowledge is not None:
        discovery = replace(
            discovery,
            use_background_knowledge=not bool(args.no_background_knowledge),
        )

    if args.alpha is not None:
        pc = replace(pc, alpha=float(args.alpha))
    if args.pc_indep_test is not None:
        pc = replace(pc, indep_test=str(args.pc_indep_test))
    if args.alpha_grid is not None:
        pc = replace(pc, alpha_grid=tuple(float(value) for value in args.alpha_grid))
    if args.pc_discrete_bins is not None:
        pc = replace(pc, discrete_bins=int(args.pc_discrete_bins))
    if args.notears_threshold is not None:
        notears = replace(notears, threshold=float(args.notears_threshold))

    if args.bootstrap_samples is not None:
        bootstrap = replace(bootstrap, samples=int(args.bootstrap_samples))
    if args.bootstrap_sample_fraction is not None:
        bootstrap = replace(
            bootstrap,
            sample_fraction=float(args.bootstrap_sample_fraction),
        )

    discovery = DiscoveryConfig(
        algorithms=discovery.algorithms,
        use_background_knowledge=discovery.use_background_knowledge,
        pc=PCConfig(
            alpha=pc.alpha,
            indep_test=pc.indep_test,
            allowed_indep_tests=pc.allowed_indep_tests,
            discrete_indep_tests=pc.discrete_indep_tests,
            discrete_bins=pc.discrete_bins,
            alpha_grid=pc.alpha_grid,
        ),
        notears=notears,
    )
    diagnostics = DiagnosticsConfig(bootstrap=bootstrap)

    merged = AnalysisConfig(
        dataset=dataset,
        run=run,
        preprocessing=preprocessing,
        discovery=discovery,
        diagnostics=diagnostics,
        reporting=analysis_config.reporting,
    )
    return AnalysisConfig.from_mapping(merged.to_dict())


def write_resolved_config(
    *,
    analysis_config: AnalysisConfig,
    feature_config: FeatureConfig,
    output_dir: Path,
) -> None:
    """再現性のために解決済み YAML 設定を保存する。

    Args:
        analysis_config: CLI 上書き後の最終 analysis 設定。
        feature_config: validation 済み特徴量設定。
        output_dir: 設定 snapshot の保存先。
    """
    write_yaml_snapshots(
        output_dir=output_dir,
        snapshots={
            "resolved_analysis_config.yaml": analysis_config.to_dict(),
            "resolved_features_config.yaml": feature_config.to_dict(),
        },
    )
