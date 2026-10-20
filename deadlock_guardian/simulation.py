"""Simülasyon motoru: process'ler kaynak ister, bırakır, bekler.  SAHİBİ: ÜYE 1.

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


class Simulation:
    def __init__(self, system):
        self.system = system

    def request(self, pname, rname, amount=1):
        """pname, rname'den amount adet ister. Verildiyse True, bekletildiyse False döner."""
        # TODO (Üye 1, Sprint 1): önce yalnızca "kaynak boş, hemen ver" durumunu yaz.
        # TODO (Üye 1, Sprint 2): bekletme (WAITING + kuyruk), doğrulamalar, log.
        raise NotImplementedError("request: Üye 1")

    def release(self, pname, rname, amount=1):
        """pname, rname'den amount adet bırakır; kuyruktaki bekleyenlere sırayla verilir."""
        # TODO (Üye 1, Sprint 2)
        raise NotImplementedError("release: Üye 1")

    def terminate(self, pname):
        """process'i sonlandırır: durumu TERMINATED, tuttuğu her şey bırakılır, bekleyenlere verilir.
        (recovery modülü bunu çağırır)"""
        # TODO (Üye 1, Sprint 2)
        raise NotImplementedError("terminate: Üye 1")
