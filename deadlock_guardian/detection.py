"""Deadlock tespiti.  SAHİBİ: ÜYE 2.   (Ders kitabı: Silberschatz Bölüm 8, deadlock detection)

Bu modüldeki fonksiyonlar System'i SADECE OKUR, değiştirmez; Simulation'a ihtiyaç yoktur.
Testleri elle kurulmuş System'lerle yapabilirsin (tests/helpers.py'a bak).
"""


def wait_for_graph(system):
    """Bekleme grafı: {process: [onu bekletenler]}.

    Bir process bir kaynağı bekliyorsa, o kaynağı TUTAN diğer process'lere bir ok çizilir.
    Sonlandırılmış process'ler grafta yoktur. Her aktif process anahtar olmalı (oku olmasa
    bile []). Listeler alfabetik ve tekrarsız.
        P1 R1'i tutuyor, P2 R1'i bekliyor  ->  {"P1": [], "P2": ["P1"]}
    """
    graf = {}
    for p in system.active_processes():
        graf[p.name] = []


    for p in system.active_processes():
        for rname in p.waiting_for:
            for q in system.active_processes():
                if q.name != p.name and q.held.get(rname, 0) > 0:
                    if q.name not in graf[p.name]:
                        graf[p.name].append(q.name)
        graf[p.name].sort()
    return graf




def find_cycle(graph):
    """Grafta bir döngü varsa döngüdeki düğümlerin listesini, yoksa None döndürür.
    DFS ile ara (düğümleri beyaz/gri/siyah işaretle). Döngünün hangi düğümden başladığı önemli değil.
        {"P1": ["P2"], "P2": ["P1"]}  ->  ["P1", "P2"]
    """
    # TODO (Üye 2, Sprint 2)
    raise NotImplementedError("find_cycle: Üye 2")


def find_deadlocked(system):
    """Deadlock'ta olan process'lerin alfabetik listesini döndürür (yoksa []).

    Çok örnekli kaynaklar için doğru olan algoritma (Silberschatz, deadlock detection):
      work = her kaynak için boştaki adet
      finish = hiçbir process bitmiş sayılmaz
      tekrarla: bitmemiş ve beklediği (waiting_for) <= work olan bir process bul;
                bulursan work += o process'in tuttukları, onu bitmiş say.
      bulunamayana kadar sürdür. Bitmemiş kalanlar deadlock'tadır.
    Bir şey beklemeyen process'in isteği boştur, yani her zaman bitebilir.
    Sonlandırılmış process'ler hesaba katılmaz.
    NOT: Grafta döngü olması deadlock olduğu anlamına GELMEZ (kaynaktan birden fazla varsa).
    """
    # TODO (Üye 2, Sprint 2)
    raise NotImplementedError("find_deadlocked: Üye 2")
