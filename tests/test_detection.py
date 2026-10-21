from deadlock_guardian.detection import wait_for_graph
from deadlock_guardian.models import TERMINATED, System
from tests.helpers import hold, wait

def klasik():
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    hold(s, "P1", "R1"); hold(s, "P2", "R2")
    wait(s, "P1", "R2"); wait(s, "P2", "R1")
    return s


def test_wait_for_graph_klasik():
    assert wait_for_graph(klasik()) == {"P1": ["P2"], "P2": ["P1"]}


def test_wait_for_graph_bekleyen_yoksa_bos_listeler():
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    hold(s, "P1", "R1")
    assert wait_for_graph(s) == {"P1": [], "P2": []}


def test_wait_for_graph_tek_bekleyen():
    s = System.create({"R1": 1}, ["P1", "P2"])
    hold(s, "P1", "R1"); wait(s, "P2", "R1")
    assert wait_for_graph(s) == {"P1": [], "P2": ["P1"]}


def test_wait_for_graph_tek_bekleyen_sonlandirilmis_yok():
    s = klasik()
    s.processes["P2"].state = TERMINATED
    assert "P2" not in wait_for_graph(s)