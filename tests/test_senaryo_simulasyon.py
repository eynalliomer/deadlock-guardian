"""Üye 1 (simülasyon) senaryoları: kuyruk, cift_deadlock.
Her senaryo gerçek modüllerle (scenario + simulation + detection + recovery) adım adım oynatılır.
"""
from pathlib import Path

from deadlock_guardian.detection import find_deadlocked
from deadlock_guardian.models import RUNNING, TERMINATED, WAITING
from deadlock_guardian.recovery import recover
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


# ---- kuyruk: FIFO, sıra atlanmaz ---------------------------------------------
def test_kuyruk_iki_process_sirayla_bekler():
    s = oynat("kuyruk.json", 3).system
    assert s.queues["R1"] == ["P2", "P3"]
    assert s.processes["P2"].state == WAITING and s.processes["P3"].state == WAITING


def test_kuyruk_bos_ornek_varken_arkadaki_sirayi_atlamaz():
    s = oynat("kuyruk.json", 4).system
    assert s.available("R1") == 1                      # P3'ün isteğine yeterdi...
    assert s.processes["P3"].state == WAITING          # ...ama baştaki P2 beklediği için alamaz
    assert s.queues["R1"] == ["P2", "P3"]


def test_kuyruk_bastaki_alinca_sira_ilerler():
    s = oynat("kuyruk.json", 5).system
    assert s.processes["P2"].held == {"R1": 2} and s.processes["P2"].state == RUNNING
    assert s.queues["R1"] == ["P3"]
    s = oynat("kuyruk.json", 6).system
    assert s.processes["P3"].held == {"R1": 1} and s.queues["R1"] == []


def test_kuyruk_sonunda_hepsi_bitti_kaynak_bos():
    s = oynat("kuyruk.json").system
    assert s.available("R1") == 2
    assert all(p.state == RUNNING and p.held == {} for p in s.processes.values())


# ---- cift_deadlock: iki bağımsız deadlock ------------------------------------
def test_cift_deadlock_once_birinci_sonra_ikinci_olusur():
    assert find_deadlocked(oynat("cift_deadlock.json", 6).system) == []
    assert find_deadlocked(oynat("cift_deadlock.json", 7).system) == ["P1", "P2"]
    assert find_deadlocked(oynat("cift_deadlock.json").system) == ["P1", "P2", "P3", "P4"]


def test_cift_deadlock_kurtarma_iki_kurban_secer():
    sim = oynat("cift_deadlock.json")
    assert recover(sim) == ["P1", "P4"]
    assert find_deadlocked(sim.system) == []


def test_cift_deadlock_terminate_kaynagi_kuyruktakine_verir():
    sim = oynat("cift_deadlock.json")
    recover(sim)
    p = sim.system.processes
    assert p["P1"].state == TERMINATED and p["P4"].state == TERMINATED
    assert p["P2"].held == {"R2": 1, "R1": 1} and p["P2"].state == RUNNING
    assert p["P3"].held == {"R3": 1, "R4": 1} and p["P3"].state == RUNNING
    assert all(q == [] for q in sim.system.queues.values())
