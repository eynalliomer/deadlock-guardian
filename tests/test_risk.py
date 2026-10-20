from deadlock_guardian.models import System 
from deadlock_guardian.risk import compute_need 
from tests.helpers import claim, hold 
def el_kitabi():    
    """Banker's örneği: R1 toplam 6, R2 toplam 4. Boşta [2, 1]."""   
    s = System.create({"R1": 6, "R2": 4}, ["P1", "P2", "P3"])    
    claim(s, "P1", {"R1": 4, "R2": 2}); hold(s, "P1", "R1", 2); hold(s, "P1", "R2", 1)   
    claim(s, "P2", {"R1": 3, "R2": 2}); hold(s, "P2", "R1", 1); hold(s, "P2", "R2", 1)    
    claim(s, "P3", {"R1": 4, "R2": 3}); hold(s, "P3", "R1", 1); hold(s, "P3", "R2", 1)   
    return s 

def test_compute_need():    
    need = compute_need(el_kitabi())   
    assert need["P1"] == {"R1": 2, "R2": 1}    
    assert need["P2"] == {"R1": 2, "R2": 1}    
    assert need["P3"] == {"R1": 3, "R2": 2}

def test_compute_need_negatif_olmaz():   
     s = System.create({"R1": 2}, ["P1"])    
     claim(s, "P1", {"R1": 1}); hold(s, "P1", "R1", 2)    
     assert compute_need(s)["P1"]["R1"] == 0 
     
def test_compute_need_bildirilmeyen_kaynak_sifir():   
     s = System.create({"R1": 1, "R2": 1}, ["P1"])    
     claim(s, "P1", {"R1": 1})    
     assert compute_need(s)["P1"] == {"R1": 1, "R2": 0}
    