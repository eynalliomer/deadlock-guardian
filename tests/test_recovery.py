import pytest

from deadlock_guardian.detection import find_deadlocked
from deadlock_guardian.models import TERMINATED, Process, System
from deadlock_guardian.recovery import choose_victim, recover, victim_cost
from deadlock_guardian.simulation import Simulation
from tests.helpers import hold


def test_victim_cost_formul():
    assert victim_cost(Process("P1", priority=1, held={"R1": 1})) == 8


def test_victim_cost_oncelik_pahali():
    assert victim_cost(Process("P1", priority=2)) == 20


def test_victim_cost_tekrar_kurban_secilen_pahali():
    assert victim_cost(Process("P1", priority=1, victim_count=2)) == 20


def test_choose_victim_en_ucuz():
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    s.processes["P2"].priority = 2
    hold(s, "P1", "R1"); hold(s, "P2", "R2")
    assert choose_victim(s, ["P1", "P2"]) == "P1"


def test_choose_victim_esitlikte_alfabetik():
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    hold(s, "P1", "R1"); hold(s, "P2", "R2")
    assert choose_victim(s, ["P2", "P1"]) == "P1"


def test_choose_victim_listede_olmayani_secmez():
    s = System.create({"R1": 1}, ["P1", "P2", "P3"])
    s.processes["P3"].priority = 0  # çok ucuz ama deadlock'ta değil
    assert choose_victim(s, ["P1", "P2"]) in ("P1", "P2")


def test_choose_victim_bos_liste_hata():
    with pytest.raises(ValueError):
        choose_victim(System.create({"R1": 1}, ["P1"]), [])


def test_recover_deadlock_cozer():
    """Bu test Üye 1 (Simulation) ve Üye 2 (find_deadlocked) bitince geçer."""
    sim = Simulation(System.create({"R1": 1, "R2": 1}, ["P1", "P2"]))
    sim.request("P1", "R1"); sim.request("P2", "R2")
    sim.request("P1", "R2"); sim.request("P2", "R1")
    assert find_deadlocked(sim.system) == ["P1", "P2"]
    assert recover(sim) == ["P1"]
    assert sim.system.processes["P1"].state == TERMINATED
    assert sim.system.processes["P2"].held == {"R2": 1, "R1": 1}
    assert find_deadlocked(sim.system) == []


def test_recover_deadlock_yoksa_bos():
    sim = Simulation(System.create({"R1": 1}, ["P1"]))
    assert recover(sim) == []