import pytest
from deadlock_guardian.models import System
from deadlock_guardian.risk import compute_need, is_request_safe, is_safe, risk_level
from tests.helpers import claim, hold, wait
def el_kitabi():
    """Banker's örneği: R1 toplam 6, R2 toplam 4. Boşta [2, 1]."""
    s = System.create({"R1": 6, "R2": 4}, ["P1", "P2", "P3"])
    claim(s, "P1", {"R1": 4, "R2": 2}); hold(s, "P1", "R1", 2); hold(s, "P1", "R2", 1)
    claim(s, "P2", {"R1": 3, "R2": 2}); hold(s, "P2", "R1", 1); hold(s, "P2", "R2", 1)
    claim(s, "P3", {"R1": 4, "R2": 3}); hold(s, "P3", "R1", 1); hold(s, "P3", "R2", 1)
    return s
def test_compute_need():
    need = compute_need(el_kitabi())
    assert need["P1"] == {"R1": 2, "R2": 1}
    assert need["P2"] == {"R1": 2, "R2": 1}
    assert need["P3"] == {"R1": 3, "R2": 2}
def test_compute_need_negatif_olmaz():
    s = System.create({"R1": 2}, ["P1"])
    claim(s, "P1", {"R1": 1}); hold(s, "P1", "R1", 2)
    assert compute_need(s)["P1"]["R1"] == 0
def test_compute_need_bildirilmeyen_kaynak_sifir():
    s = System.create({"R1": 1, "R2": 1}, ["P1"])
    claim(s, "P1", {"R1": 1})
    assert compute_need(s)["P1"] == {"R1": 1, "R2": 0}
def guvensiz():
    """İkisi de bir kaynağı tutuyor ve ikisine de ihtiyacı var, boşta hiçbir şey yok."""
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    claim(s, "P1", {"R1": 1, "R2": 1}); claim(s, "P2", {"R1": 1, "R2": 1})
    hold(s, "P1", "R1"); hold(s, "P2", "R2")
    return s
def test_is_safe_el_kitabi():
    assert is_safe(el_kitabi()) == (True, ["P1", "P2", "P3"])
def test_is_safe_guvensiz():
    assert is_safe(guvensiz()) == (False, [])
def test_is_request_safe_guvenli_istek():
    assert is_request_safe(el_kitabi(), "P1", "R1", 1) is True
def test_is_request_safe_guvensiz_istek():
    assert is_request_safe(el_kitabi(), "P3", "R1", 1) is False
def test_is_request_safe_sistemi_degistirmez():
    s = el_kitabi()
    is_request_safe(s, "P1", "R1", 1)
    assert s.processes["P1"].held == {"R1": 2, "R2": 1}
    assert s.available("R1") == 2
def test_is_request_safe_ihtiyactan_fazla_hata():
    with pytest.raises(ValueError):
        is_request_safe(el_kitabi(), "P1", "R1", 3)
def test_is_request_safe_bostan_fazla_istek_false():
    assert is_request_safe(guvensiz(), "P1", "R2", 1) is False
def test_risk_low():
    level, reason = risk_level(el_kitabi(), [])
    assert level == "LOW" and reason
def test_risk_medium_bekleyen_var():
    s = System.create({"R1": 2}, ["P1", "P2"])
    claim(s, "P1", {"R1": 2}); claim(s, "P2", {"R1": 1})
    hold(s, "P1", "R1", 2); wait(s, "P2", "R1")
    level, reason = risk_level(s, [])
    assert level == "MEDIUM" and "P2" in reason
def test_risk_medium_bos_kaynak_az():
    s = System.create({"R1": 10}, ["P1"])
    claim(s, "P1", {"R1": 9}); hold(s, "P1", "R1", 9)
    assert risk_level(s, [])[0] == "MEDIUM"
def test_risk_high_guvensiz_durum():
    level, reason = risk_level(guvensiz(), [])
    assert level == "HIGH" and reason
def test_risk_critical_deadlock():
    level, reason = risk_level(guvensiz(), ["P1", "P2"])
    assert level == "CRITICAL" and "P1" in reason and "P2" in reason