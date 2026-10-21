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
from .models import RUNNING

class Simulation:
    def __init__(self, system):
        self.system = system

    def request(self, pname, rname, amount=1):
        p = self.system.processes[pname]
        if self.system.available(rname) >= amount:
            p.held[rname] = p.held.get(rname, 0) + amount
            p.state = RUNNING
            self.system.log.append(f"{pname} REQUEST {rname} x{amount} -> GRANTED")
            return True

        raise NotImplementedError("request() henüz tamamlanmadı")
          
            
            

