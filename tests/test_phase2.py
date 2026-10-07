from app.analytics.evaluation import compare_baselines
from app.analytics.simulation import compare_policies


def test_baseline_evaluation_returns_metrics():
    result = compare_baselines([1, 2, 3, 4, 5, 4, 3])
    assert result
    assert all("mae" in row and "smape" in row for row in result)


def test_policy_simulation_returns_baseline_and_dynamic():
    result = compare_policies([8, 10, 2, 12, 4, 9], 10, 5, 10)
    assert [row["policy"] for row in result] == ["fixed_threshold", "dynamic_forecast"]
    assert all(0 <= row["service_level"] <= 1 for row in result)
