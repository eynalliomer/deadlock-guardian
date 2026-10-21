from deadlock_guardian.models import RUNNING , System
from deadlock_guardian.simulation import Simulation
def make(resources=None, processes=("P1", "P2")):
    return Simulation(System.create(resources or {"R1": 1, "R2": 2}, processes))
def test_bos_kaynak_hemen_verilir():
    sim = make()
    assert sim.request("P1", "R1") is True
    p = sim.system.processes["P1"]
    assert p.held == {"R1": 1} and p.state == RUNNING
    assert sim.system.available("R1") == 0