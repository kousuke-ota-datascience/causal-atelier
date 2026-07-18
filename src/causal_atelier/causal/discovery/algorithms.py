from __future__ import annotations

import pandas as pd

from .graph import (
    graph_edge_records,
    weight_matrix_edge_records,
)

from .constants import DEFAULT_ALPHA_GRID, DEFAULT_DISCRETE_PC_INDEP_TESTS, DEFAULT_PC_INDEP_TESTS
from causal_atelier.preprocessing.discovery.config import FeatureConfig

from .results import DiscoveryResult


class CausalDiscovery:
    """標準化済み特徴量フレームに対して因果探索アルゴリズムを実行する。

    Args:
        alpha: Main PC significance level.
        use_background_knowledge: Whether to apply temporal tier constraints.
        feature_config: Feature configuration used to construct tiers.
        algorithms: Algorithms to run.
        notears_threshold: Absolute weight threshold for NOTEARS edges.
        pc_indep_test: Conditional-independence test name for PC.
        allowed_pc_indep_tests: Supported PC test names.
        discrete_pc_indep_tests: PC tests that require discretized input.
        alpha_grid: Alpha values for PC sensitivity analysis.
        bootstrap_samples: Number of bootstrap samples for PC stability.
        bootstrap_sample_fraction: Fraction of rows sampled per bootstrap.
        random_seed: Random seed for bootstrap sampling.
        pc_discrete_bins: Number of quantile bins for discrete PC tests.
    """

    def __init__(
        self,
        *,
        alpha: float,
        use_background_knowledge: bool,
        feature_config: FeatureConfig,
        algorithms: tuple[str, ...] = ("pc", "ges", "lingam", "notears"),
        notears_threshold: float = 0.3,
        pc_indep_test: str = "fisherz",
        allowed_pc_indep_tests: tuple[str, ...] = DEFAULT_PC_INDEP_TESTS,
        discrete_pc_indep_tests: tuple[str, ...] = DEFAULT_DISCRETE_PC_INDEP_TESTS,
        alpha_grid: tuple[float, ...] = DEFAULT_ALPHA_GRID,
        bootstrap_samples: int = 100,
        bootstrap_sample_fraction: float = 1.0,
        random_seed: int = 20260630,
        pc_discrete_bins: int = 4,
    ) -> None:
        """探索 runner を初期化し、アルゴリズム設定を検証する。

        Args:
            alpha: Main PC significance level.
            use_background_knowledge: Whether to apply temporal tier constraints.
            feature_config: Feature configuration used to construct tiers.
            algorithms: Algorithms to run.
            notears_threshold: Absolute weight threshold for NOTEARS edges.
            pc_indep_test: Conditional-independence test name for PC.
            allowed_pc_indep_tests: Supported PC test names.
            discrete_pc_indep_tests: PC tests that require discretized input.
            alpha_grid: Alpha values for PC sensitivity analysis.
            bootstrap_samples: Number of bootstrap samples for PC stability.
            bootstrap_sample_fraction: Fraction of rows sampled per bootstrap.
            random_seed: Random seed for bootstrap sampling.
            pc_discrete_bins: Number of quantile bins for discrete PC tests.

        Raises:
            ValueError: If PC or bootstrap settings are outside supported ranges.
        """
        if pc_indep_test not in allowed_pc_indep_tests:
            raise ValueError(
                f"pc_indep_test must be one of {allowed_pc_indep_tests}: {pc_indep_test}"
            )
        if bootstrap_samples < 0:
            raise ValueError("bootstrap_samples must be non-negative")
        if not 0 < bootstrap_sample_fraction <= 1:
            raise ValueError("bootstrap_sample_fraction must be in (0, 1]")
        if pc_discrete_bins < 2:
            raise ValueError("pc_discrete_bins must be at least 2")

        self.alpha = alpha
        self.use_background_knowledge = use_background_knowledge
        self.feature_config = feature_config
        self.algorithms = tuple(algorithms)
        self.notears_threshold = notears_threshold
        self.pc_indep_test = pc_indep_test
        self.allowed_pc_indep_tests = allowed_pc_indep_tests
        self.discrete_pc_indep_tests = discrete_pc_indep_tests
        self.alpha_grid = tuple(sorted({float(value) for value in (*alpha_grid, alpha)}))
        self.bootstrap_samples = bootstrap_samples
        self.bootstrap_sample_fraction = bootstrap_sample_fraction
        self.random_seed = random_seed
        self.pc_discrete_bins = pc_discrete_bins

    def run_all(self, frame: pd.DataFrame) -> dict[str, DiscoveryResult]:
        """設定された全アルゴリズムを実行する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Mapping from algorithm name to discovery result. Import failures
            and algorithm errors are captured in the result status.
        """
        runners = {
            "pc": self.run_pc,
            "ges": self.run_ges,
            "lingam": self.run_lingam,
            "notears": self.run_notears,
        }
        results = {}
        for algorithm in self.algorithms:
            runner = runners[algorithm]
            try:
                causal_graph, edges = runner(frame)
                results[algorithm] = DiscoveryResult(
                    algorithm=algorithm,
                    causal_graph=causal_graph,
                    edges=edges,
                    status="ok",
                    message="",
                )
            except ImportError as exc:
                results[algorithm] = DiscoveryResult(
                    algorithm=algorithm,
                    causal_graph=None,
                    edges=pd.DataFrame(
                        columns=["source", "target", "endpoint_source", "endpoint_target", "edge"]
                    ),
                    status="skipped",
                    message=str(exc),
                )
            except Exception as exc:
                results[algorithm] = DiscoveryResult(
                    algorithm=algorithm,
                    causal_graph=None,
                    edges=pd.DataFrame(
                        columns=["source", "target", "endpoint_source", "endpoint_target", "edge"]
                    ),
                    status="failed",
                    message=f"{type(exc).__name__}: {exc}",
                )
        return results

    def run_pc(self, frame: pd.DataFrame, *, alpha: float | None = None):
        """PC アルゴリズムを実行する。

        Args:
            frame: Standardized discovery input.
            alpha: Optional PC alpha overriding the instance default.

        Returns:
            Pair of causal-learn graph object and normalized edge records.
        """
        from causallearn.search.ConstraintBased.PC import pc

        pc_frame = self.prepare_pc_frame(frame)
        node_names = list(pc_frame.columns)
        background_knowledge = (
            self.build_background_knowledge(node_names)
            if self.use_background_knowledge
            else None
        )
        causal_graph = pc(
            pc_frame.to_numpy(),
            alpha=self.alpha if alpha is None else alpha,
            indep_test=self.pc_indep_test,
            stable=True,
            background_knowledge=background_knowledge,
            node_names=node_names,
            show_progress=False,
        )
        return causal_graph, graph_edge_records(causal_graph.G)

    def prepare_pc_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        """選択された独立性検定に合わせて PC 入力を準備する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Original frame for continuous tests, or discretized frame for
            discrete tests such as ``chisq`` and ``gsq``.
        """
        if self.pc_indep_test not in self.discrete_pc_indep_tests:
            return frame

        return pd.DataFrame(
            {column: self.discretize_series(frame[column]) for column in frame.columns},
            index=frame.index,
        )

    def discretize_series(self, series: pd.Series) -> pd.Series:
        """離散 PC 検定用に series を quantile discretization する。

        Args:
            series: Numeric input series.

        Returns:
            Integer-coded series with at most ``pc_discrete_bins`` bins.
        """
        non_null = series.dropna()
        unique_values = non_null.nunique()
        if unique_values <= 1:
            return pd.Series([0] * len(series), index=series.index, dtype=int)
        if unique_values <= 2:
            codes = pd.Categorical(series).codes
            return pd.Series(codes, index=series.index).astype(int)

        bins = min(self.pc_discrete_bins, unique_values)
        ranked = series.rank(method="average")
        binned = pd.qcut(ranked, q=bins, labels=False, duplicates="drop")
        return pd.Series(binned, index=series.index).fillna(0).astype(int)

    def run_ges(self, frame: pd.DataFrame):
        """GES の score-based search を実行する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Pair of causal-learn graph object and normalized edge records.
        """
        from causallearn.search.ScoreBased.GES import ges

        result = ges(
            frame.to_numpy(),
            score_func="local_score_marginal_general",
            node_names=list(frame.columns),
        )
        causal_graph = result["G"]
        return causal_graph, graph_edge_records(causal_graph)

    def run_lingam(self, frame: pd.DataFrame):
        """DirectLiNGAM を実行する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Pair of fitted LiNGAM model and weighted edge records.

        Raises:
            ImportError: If the optional ``lingam`` package is unavailable.
        """
        try:
            from lingam import DirectLiNGAM
        except ImportError as exc:
            raise ImportError(
                "LiNGAM requires the optional `lingam` package. Install it before running this algorithm."
            ) from exc

        model = DirectLiNGAM()
        model.fit(frame.to_numpy())
        edges = weight_matrix_edge_records(
            model.adjacency_matrix_,
            node_names=list(frame.columns),
            threshold=0.0,
        )
        return model, edges

    def run_notears(self, frame: pd.DataFrame):
        """線形 NOTEARS 実装を実行する。

        Args:
            frame: Standardized discovery input.

        Returns:
            Pair of weight matrix and weighted edge records.

        Raises:
            ImportError: If a compatible NOTEARS package is unavailable.
        """
        try:
            from notears.linear import notears_linear
        except ImportError as exc:
            raise ImportError(
                "NOTEARS requires an optional NOTEARS implementation such as the `notears` package. "
                "Install it before running this algorithm."
            ) from exc

        weight_matrix = notears_linear(frame.to_numpy(), lambda1=0.1, loss_type="l2")
        edges = weight_matrix_edge_records(
            weight_matrix,
            node_names=list(frame.columns),
            threshold=self.notears_threshold,
        )
        return weight_matrix, edges

    def build_background_knowledge(self, node_names: list[str]):
        """feature tier から causal-learn の background knowledge を構築する。

        Args:
            node_names: Variables retained in the discovery input.

        Returns:
            causal-learn ``BackgroundKnowledge`` object with tier assignments.
        """
        from causallearn.graph.GraphNode import GraphNode
        from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge

        background_knowledge = BackgroundKnowledge()
        nodes = {name: GraphNode(name) for name in node_names}

        for tier_index, tier_names in enumerate(
            self.feature_config.background_tiers_for_nodes(node_names)
        ):
            for name in sorted(tier_names):
                background_knowledge.add_node_to_tier(nodes[name], tier_index)

        return background_knowledge
