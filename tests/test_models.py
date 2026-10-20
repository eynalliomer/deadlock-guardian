from deadlock_guardian.models import RUNNING, Process, System
from tests.helpers import hold


def test_create_kurar():
    s = System.create({"R1": 1, "R2": 2}, ["P1", "P2"])
    assert set(s.processes) == {"P1", "P2"}
    assert s.resources["R2"].total == 2
    assert s.queues == {"R1": [], "R2": []}


def test_process_varsayilanlari():
    p = Process("P1")
    assert p.state == RUNNING and p.held == {} and p.waiting_for == {} and p.max_claim == {}


def test_process_sozlukleri_birbirinden_bagimsiz():
    a, b = Process("P1"), Process("P2")
    a.held["R1"] = 1
    assert b.held == {}


def test_available_bos_kaynak():
    s = System.create({"R1": 1}, ["P1"])
    assert s.available("R1") == 1


def test_available_dolu_kaynak():
    s = System.create({"R1": 1}, ["P1"])
    hold(s, "P1", "R1")
    assert s.available("R1") == 0


def test_available_cok_ornekli():
    s = System.create({"R1": 3}, ["P1", "P2"])
    hold(s, "P1", "R1", 1)
    hold(s, "P2", "R1", 1)
    assert s.available("R1") == 1
