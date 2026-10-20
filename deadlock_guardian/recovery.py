"""Kurtarma (recovery): deadlock'tan çıkmak için kurban seçip sonlandırmak.  SAHİBİ: ÜYE 4.
(Ders kitabı: Silberschatz Bölüm 8, recovery from deadlock)
"""


def victim_cost(process):
    toplam = sum(process.held.values())
    return process.priority * 10 - 2 * toplam + 5 * process.victim_count


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
