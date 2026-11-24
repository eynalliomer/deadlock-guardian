from pathlib import Path

from deadlock_guardian.detection import find_cycle, find_deadlocked, wait_for_graph
from deadlock_guardian.models import RUNNING, TERMINATED, WAITING
from deadlock_guardian.recovery import choose_victim, recover
from deadlock_guardian.scenario import load_scenario
from deadlock_guardian.simulation import Simulation

SENARYOLAR = Path(__file__).resolve().parent.parent / "scenarios"

def oynat(ad, adim_sayisi=None):
    system, steps = load_scenario(SENARYOLAR / ad)
    sim = Simulation(system)
    for process, action, resource, amount in steps[:adim_sayisi]:
        if action == "request":
            sim.request(process, resource, amount)
        else:
            sim.release(process, resource, amount)
    return sim

#cok_ornekli: dongu var ama deadlock yok
def test_cok_ornekli_dongu_var_ama_deadlock_yok():
    s = oynat("cok_ornekli.json", 6).system
    assert find_cycle(wait_for_graph(s)) == ["P1", "P3"]
    assert find_deadlocked(s) == []


def test_cok_ornekli_dongu_bekleyenler_kaynak_alinca_cozulur():
    s = oynat("cok_ornekli.json").system
    assert find_cycle(wait_for_graph(s)) is None
    assert all(p.state == RUNNING for p in s.processes.values())


#zincir: dongude degil ama deadlock
def test_zincir_p3_dongude_degil_ama_deadlockta():
    s = oynat("zincir.json").system
    assert find_cycle(wait_for_graph(s)) == ["P1", "P2"]
    assert find_deadlocked(s) == ["P1", "P2", "P3"]


def test_zincir_kurtarma_r1_kuyruktaki_p3e_gecer():
    sim = oynat("zincir.json")
    assert recover(sim) == ["P1"]
    s = sim.system
    assert s.processes["P3"].held == {"R1": 1} and s.processes["P3"].state == RUNNING
    assert s.processes["P2"].state == WAITING
    assert find_deadlocked(s) == []


#uclu_deadlock: uc processli dongu
def test_uclu_deadlock_son_adimdan_once_deadlock_yok():
    s = oynat("uclu_deadlock.json", 5).system
    assert find_deadlocked(s) == []


def test_uclu_deadlock_uc_process_dongude():
    s = oynat("uclu_deadlock.json").system
    assert wait_for_graph(s) == {"P1": ["P2"], "P2": ["P3"], "P3": ["P1"]}
    assert find_cycle(wait_for_graph(s)) == ["P1", "P2", "P3"]
    assert find_deadlocked(s) == ["P1", "P2", "P3"]


def test_uclu_deadlock_en_dusuk_oncelikli_p2_kurban():
    sim = oynat("uclu_deadlock.json")
    assert choose_victim(sim.system, find_deadlocked(sim.system)) == "P2"
    assert recover(sim) == ["P2"]
    assert sim.system.processes["P2"].state == TERMINATED
    assert find_deadlocked(sim.system) == []


