import pytest

from relmote.power import PowerBudget, PowerLoad, ideal_runtime_hours


def test_budget_reserves_safety_margin():
    budget = PowerBudget(available_mw=12000, reserve_mw=3000)
    loads = [
        PowerLoad("core", typical_mw=2000, peak_mw=3000),
        PowerLoad("kvm", typical_mw=3000, peak_mw=4000),
        PowerLoad("lora", typical_mw=300, peak_mw=1800),
    ]

    assert budget.admit(loads)
    assert budget.remaining_mw(loads) == 200


def test_peak_budget_can_reject_configuration_typical_would_allow():
    budget = PowerBudget(available_mw=5000, reserve_mw=500)
    loads = [
        PowerLoad("core", typical_mw=1500, peak_mw=2500),
        PowerLoad("cellular", typical_mw=1200, peak_mw=3000),
    ]

    assert budget.admit(loads, use_peak=False)
    assert not budget.admit(loads, use_peak=True)


def test_ideal_runtime_is_simple_capacity_over_load():
    assert ideal_runtime_hours(20, 2) == 10


def test_invalid_power_load_fails():
    with pytest.raises(ValueError):
        PowerLoad("bad", typical_mw=2000, peak_mw=1000)
