from deadlock_guardian.detection import find_cycle, find_deadlocked, wait_for_graph
from deadlock_guardian.models import TERMINATED, System
from tests.helpers import hold, wait


def klasik():
    """P1 R1'i tutup R2'yi, P2 R2'yi tutup R1'i bekliyor."""
    s = System.create({"R1": 1, "R2": 1}, ["P1", "P2"])
    hold(s, "P1", "R1"); hold(s, "P2", "R2")
    wait(s, "P1", "R2"); wait(s, "P2", "R1")
    return s


#wait for graph
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


#find cycle
def test_find_cycle_var():
    c = find_cycle({"P1": ["P2"], "P2": ["P1"]})
    assert c is not None and set(c) == {"P1", "P2"}


def test_find_cycle_yok():
    assert find_cycle({"P1": ["P2"], "P2": []}) is None


def test_find_cycle_uclu():
    c = find_cycle({"P1": ["P2"], "P2": ["P3"], "P3": ["P1"]})
    assert set(c) == {"P1", "P2", "P3"}


def test_find_cycle_dongu_disindaki_dugum_dahil_olmaz():
    c = find_cycle({"P0": ["P1"], "P1": ["P2"], "P2": ["P1"]})
    assert set(c) == {"P1", "P2"}


#find deadlocked
def test_find_deadlocked_klasik():
    assert find_deadlocked(klasik()) == ["P1", "P2"]


def test_find_deadlocked_hic_bekleyen_yok():
    s = System.create({"R1": 1}, ["P1", "P2"])
    hold(s, "P1", "R1")
    assert find_deadlocked(s) == []


def test_find_deadlocked_disarida_kalan_process_dahil_degil():
    s = System.create({"R1": 1, "R2": 1, "R3": 1}, ["P1", "P2", "P3"])
    hold(s, "P1", "R1"); hold(s, "P2", "R2"); hold(s, "P3", "R3")
    wait(s, "P1", "R2"); wait(s, "P2", "R1")
    assert find_deadlocked(s) == ["P1", "P2"]


def cok_ornek(p1_ek_istek):
    """Çok örnekli kaynak örneği: R1 (yazıcı) x3, R2 (tarayıcı) x2."""
    s = System.create({"R1": 3, "R2": 2}, ["P1", "P2", "P3"])
    hold(s, "P1", "R1")
    hold(s, "P2", "R1"); hold(s, "P2", "R2")
    hold(s, "P3", "R1"); hold(s, "P3", "R2")
    wait(s, "P2", "R1")
    wait(s, "P3", "R2")
    if p1_ek_istek:
        wait(s, "P1", "R2")
    return s


def test_find_deadlocked_cok_ornekli_deadlock_yok():
    assert find_deadlocked(cok_ornek(False)) == []


def test_find_deadlocked_cok_ornekli_deadlock_var():
    assert find_deadlocked(cok_ornek(True)) == ["P1", "P2", "P3"]


def test_dongu_var_ama_deadlock_yok():
    """R1'in 2 adedi var, P3 bitince boşalır."""
    s = System.create({"R1": 2, "R2": 1}, ["P1", "P2", "P3"])
    hold(s, "P1", "R2")
    hold(s, "P2", "R1")
    hold(s, "P3", "R1")
    wait(s, "P1", "R1")
    wait(s, "P2", "R2")
    assert find_cycle(wait_for_graph(s)) is not None   # grafta döngü var...
    assert find_deadlocked(s) == []                    # ...ama deadlock yok