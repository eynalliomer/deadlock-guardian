from deadlock_guardian.models import Process
from deadlock_guardian.recovery import victim_cost

def test_victim_cost_formul ():
    assert victim_cost(Process("P1", priority=1, held={"R1": 1})) == 8


def test_victim_cost_oncelik_pahali ():
    assert victim_cost(Process("P1", priority=2)) == 20

def test_victim_cost_tekrar_kurban_secilen_pahali():
    assert victim_cost(Process("P1", priority=1, victim_count=2)) == 20