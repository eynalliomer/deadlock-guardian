"""Üye 3 (risk) senaryoları: bankers, guvensiz.
Her senaryo gerçek modüllerle (scenario + simulation + detection + risk) adım adım oynatılır.
"""

from pathlib import Path

from deadlock_guardian.detection import find_deadlocked
from deadlock_guardian.risk import compute_need, is_request_safe, is_safe, risk_level
from deadlock_guardian.scenario import load_scenario
from deadlock_guardian.simulation import Simulation

SENARYOLAR = Path(__file__).resolve().parent.parent / "scenarios"


def oynat(ad, adim_sayisi=None):
    """Senaryoyu yükler ve ilk adim_sayisi adımı (verilmezse hepsini) çalıştırır."""
    system, steps = load_scenario(SENARYOLAR / ad)
    sim = Simulation(system)
    for process, action, resource, amount in steps[:adim_sayisi]:
        if action == "request":
            sim.request(process, resource, amount)
        else:
            sim.release(process, resource, amount)
    return sim


def seviyeler(ad):
    """Her adımdan sonraki risk seviyesi."""
    system, steps = load_scenario(SENARYOLAR / ad)
    sim = Simulation(system)
    sonuc = []
    for process, action, resource, amount in steps:
        if action == "request":
            sim.request(process, resource, amount)
        else:
            sim.release(process, resource, amount)
        sonuc.append(risk_level(system, find_deadlocked(system))[0])
    return sonuc


# ---- bankers: ders kitabı örneği --------------------------------------------

def test_bankers_6_adim_sonra_ders_kitabi_durumu():
    s = oynat("bankers.json", 6).system
    assert s.available("R1") == 2 and s.available("R2") == 1
    assert compute_need(s) == {
        "P1": {"R1": 2, "R2": 1},
        "P2": {"R1": 2, "R2": 1},
        "P3": {"R1": 3, "R2": 2},
    }
    assert is_safe(s) == (True, ["P1", "P2", "P3"])


def test_bankers_7_adimdaki_istek_guvenli():
    s = oynat("bankers.json", 6).system
    assert is_request_safe(s, "P1", "R1", 1) is True
    assert is_safe(oynat("bankers.json", 7).system)[0] is True


def test_bankers_8_adimdaki_istek_guvensiz():
    s = oynat("bankers.json", 7).system
    assert is_request_safe(s, "P3", "R1", 1) is False
    assert is_safe(oynat("bankers.json").system) == (False, [])


def test_bankers_risk_seviyeleri():
    assert seviyeler("bankers.json") == ["LOW"] * 7 + ["HIGH"]


# ---- guvensiz: güvensiz durum deadlock demek değildir -----------------------

def test_guvensiz_ikinci_adimda_guvensiz_ama_deadlock_yok():
    s = oynat("guvensiz.json", 2).system
    assert is_safe(s) == (False, [])
    assert find_deadlocked(s) == []
    assert risk_level(s, [])[0] == "HIGH"


def test_guvensiz_son_adimda_deadlock():
    s = oynat("guvensiz.json").system
    assert find_deadlocked(s) == ["P1", "P2"]


def test_guvensiz_risk_seviyeleri():
    assert seviyeler("guvensiz.json") == ["LOW", "HIGH", "HIGH", "HIGH", "CRITICAL"]