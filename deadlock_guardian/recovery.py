"""Kurtarma (recovery): deadlock'tan çıkmak için kurban seçip sonlandırmak.  SAHİBİ: ÜYE 4.
(Ders kitabı: Silberschatz Bölüm 8, recovery from deadlock)
"""


def victim_cost(process):
    """Process'in kurban seçilme maliyeti (düşük = önce o sonlandırılır).
        maliyet = öncelik*10  -  2 * (tuttuğu toplam adet)  +  5 * victim_count
    Örn: priority=1, held={"R1": 1}, victim_count=0  ->  10 - 2 + 0 = 8"""
    # TODO (Üye 4, Sprint 1)
    raise NotImplementedError("victim_cost: Üye 4")


def choose_victim(system, deadlocked):
    """deadlocked (process adları) arasından en düşük maliyetli olanı döndürür.
    Maliyet eşitse alfabetik olarak ilk isim. Liste boşsa ValueError."""
    # TODO (Üye 4, Sprint 2)
    raise NotImplementedError("choose_victim: Üye 4")


def recover(sim):
    """Deadlock bitene kadar: find_deadlocked -> choose_victim -> victim_count += 1 -> sim.terminate.
    Sonlandırılan process adlarını sırayla (liste) döndürür. Deadlock yoksa [].
    (Bu fonksiyon Üye 1'in terminate'ine ve Üye 2'nin find_deadlocked'ine dayanır; onlar bitince çalışır.)"""
    # TODO (Üye 4, Sprint 2)
    raise NotImplementedError("recover: Üye 4")
