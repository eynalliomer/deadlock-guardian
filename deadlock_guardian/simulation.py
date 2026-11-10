"""Simülasyon motoru: process'ler kaynak ister, bırakır, bekler.  SAHİBİ: eynalliomer.

System (models.py) sadece veriyi tutar; durumu DEĞİŞTİREN her şey burada yapılır.
Kurallar:
  - Kaynak yeterliyse (boş >= istenen) hemen verilir: process.held artar, durum RUNNING.
  - Yetmiyorsa process WAITING olur: process.waiting_for = {kaynak: adet}, ve
    system.queues[kaynak] listesinin SONUNA adı eklenir. request False döner.
  - release sonrası kuyruk BAŞTAN okunur: baştaki process'in isteği karşılanabiliyorsa verilir
    ve kuyruktan çıkar; karşılanamıyorsa DURULUR (kuyruktan atlama yok).
  - Her olay system.log'a bir metin satırı olarak eklenir (örn. "P1 REQUEST R1 x1 -> GRANTED").
  - Geçersiz işlemde ValueError: bilinmeyen process/kaynak, sonlandırılmış ya da bekleyen
    process'in yeni istek yapması, adet < 1 ya da kaynağın toplamından fazla, tutandan fazla bırakma.
"""
from .models import RUNNING, WAITING, TERMINATED


class Simulation:
    def __init__(self, system):
        self.system = system

    def request(self, pname, rname, amount=1):
        if pname not in self.system.processes:
            raise ValueError(f"Bilinmeyen process: {pname}")
        if rname not in self.system.resources:
            raise ValueError(f"Bilinmeyen kaynak: {rname}")
        if amount < 1 or amount > self.system.resources[rname].total:
            raise ValueError(f"Geçersiz adet: {amount}")

        p = self.system.processes[pname]

        if p.state == TERMINATED:
            raise ValueError(f"{pname} sonlandırılmış, istek yapamaz")
        if p.state == WAITING:
            raise ValueError(f"{pname} zaten bekliyor, yeni istek yapamaz")

        if self.system.available(rname) >= amount:
            p.held[rname] = p.held.get(rname, 0) + amount
            p.state = RUNNING
            self.system.log.append(f"{pname} REQUEST {rname} x{amount} -> GRANTED")
            return True

        p.state = WAITING
        p.waiting_for = {rname: amount}
        self.system.queues[rname].append(pname)
        self.system.log.append(f"{pname} REQUEST {rname} x{amount} -> WAITING")
        return False

    def release(self, pname, rname, amount=1):
        if pname not in self.system.processes:
            raise ValueError(f"Bilinmeyen process: {pname}")
        if rname not in self.system.resources:
            raise ValueError(f"Bilinmeyen kaynak: {rname}")

        p = self.system.processes[pname]

        if p.held.get(rname, 0) < amount:
            raise ValueError(f"{pname}, {rname} kaynağından {amount} adet tutmuyor")

        p.held[rname] -= amount
        if p.held[rname] == 0:
            del p.held[rname]

        self.system.log.append(f"{pname} RELEASE {rname} x{amount}")

        kuyruk = self.system.queues[rname]
        while kuyruk:
            bekleyen_adi = kuyruk[0]
            bekleyen = self.system.processes[bekleyen_adi]
            istenen = bekleyen.waiting_for[rname]
            if self.system.available(rname) < istenen:
                break
            kuyruk.pop(0)
            bekleyen.held[rname] = bekleyen.held.get(rname, 0) + istenen
            bekleyen.waiting_for = {}
            bekleyen.state = RUNNING
            self.system.log.append(f"{bekleyen_adi} GRANTED {rname} x{istenen} (kuyruktan)")

    def terminate(self, pname):
        if pname not in self.system.processes:
            raise ValueError(f"Bilinmeyen process: {pname}")

        p = self.system.processes[pname]

        for kuyruk in self.system.queues.values():
            if pname in kuyruk:
                kuyruk.remove(pname)

        biraktiklari = list(p.held.keys())

        p.held = {}
        p.waiting_for = {}
        p.state = TERMINATED
        self.system.log.append(f"{pname} TERMINATED")

        for rname in biraktiklari:
            kuyruk = self.system.queues[rname]
            while kuyruk:
                bekleyen_adi = kuyruk[0]
                bekleyen = self.system.processes[bekleyen_adi]
                istenen = bekleyen.waiting_for[rname]
                if self.system.available(rname) < istenen:
                    break
                kuyruk.pop(0)
                bekleyen.held[rname] = bekleyen.held.get(rname, 0) + istenen
                bekleyen.waiting_for = {}
                bekleyen.state = RUNNING
                self.system.log.append(f"{bekleyen_adi} GRANTED {rname} x{istenen} (kuyruktan)")
