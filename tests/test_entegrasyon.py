"""Entegrasyon testleri: tüm modüller (scenario, simulation, detection, risk, recovery, demo) birlikte.
scenarios/ klasöründeki HER senaryo otomatik bulunur; yeni senaryo eklenince bu testler onu da kapsar.
"""
from pathlib import Path

import pytest

from deadlock_guardian.demo import main
from deadlock_guardian.detection import find_deadlocked
from deadlock_guardian.recovery import recover
from deadlock_guardian.risk import risk_level
from deadlock_guardian.scenario import load_scenario
from deadlock_guardian.simulation import Simulation

SENARYOLAR = sorted((Path(__file__).resolve().parent.parent / "scenarios").glob("*.json"))
IDLER = [p.stem for p in SENARYOLAR]


def calistir(path):
    """demo.py'deki akışın aynısı: adımı uygula, deadlock varsa kurtar. Kurbanların listesini döndürür."""
    system, steps = load_scenario(path)
    sim = Simulation(system)
    kurbanlar = []
    for process, action, resource, amount in steps:
        if action == "request":
            sim.request(process, resource, amount)
        else:
            sim.release(process, resource, amount)
        if find_deadlocked(system):
            kurbanlar += recover(sim)
    return system, kurbanlar


def test_senaryo_klasoru_bos_degil():
    assert len(SENARYOLAR) >= 2


@pytest.mark.parametrize("path", SENARYOLAR, ids=IDLER)
def test_demo_her_senaryoda_hatasiz_biter(path, capsys):
    assert main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "Senaryo:" in out and "RISK" in out


@pytest.mark.parametrize("path", SENARYOLAR, ids=IDLER)
def test_senaryo_sonunda_deadlock_kalmaz(path):
    system, kurbanlar = calistir(path)
    assert find_deadlocked(system) == []


@pytest.mark.parametrize("path", SENARYOLAR, ids=IDLER)
def test_risk_seviyesi_gecerli_ve_nedeni_dolu(path):
    system, _ = calistir(path)
    seviye, neden = risk_level(system, find_deadlocked(system))
    assert seviye in ("LOW", "MEDIUM", "HIGH", "CRITICAL") and neden


def test_deadlock_senaryosu_kurtarmada_bir_kurban_verir():
    system, kurbanlar = calistir("scenarios/deadlock.json")
    assert len(kurbanlar) == 1
    assert system.processes[kurbanlar[0]].state == "TERMINATED"


def test_normal_senaryoda_kurban_yok():
    system, kurbanlar = calistir("scenarios/normal.json")
    assert kurbanlar == []
