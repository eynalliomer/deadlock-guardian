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


def ulasilabilir(graph, bas):
    "bas dügümünden baslayip oklari izleyerek gidilebilen tüm dügümler"
    gidilenler = []
    gidilecekler = list(graph[bas])
    while gidilecekler:
        d = gidilecekler.pop()
        if d not in gidilenler:
            gidilenler.append(d)
            gidilecekler.extend(graph[d])
    return gidilenler


def find_cycle(graph):
    """Grafta bir döngü varsa döngüdeki düğümlerin listesini, yoksa None döndürür"""
    for d in graph:
        if d in ulasilabilir(graph, d): #kendine geri donebiliyorsa dongude
            dongu = []
            for x in ulasilabilir(graph, d):
                if d in ulasilabilir(graph, x): #x de d'ye geri donebiliyor mu?
                    dongu.append(x)
            return sorted(dongu)
    return None   


def sigiyor(p, work):
    "p'nin bekledigi her sey, bostaki kaynaklara sigiyor mu?"
    for rname, adet in p.waiting_for.items():
        if adet > work[rname]:
            return False
    return True


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
    work = {}
    for rname in system.resources:
        work[rname] = system.available(rname)

    kalan = list(system.active_processes())
    degisti = True
    while degisti:
        degisti = False
        for p in kalan:
            if sigiyor(p, work): #bu process bitebilir
                for rname, adet in p.held.items():
                    work[rname] = work[rname] + adet #bitince tuttuklarini geri verir
                kalan.remove(p)
                degisti = True
                break
    sonuc = []
    for p in kalan:
        sonuc.append(p.name)
    return sorted(sonuc)
