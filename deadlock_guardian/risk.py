"""Risk analizi: Banker's Algorithm ve risk seviyeleri.  SAHİBİ: ÜYE 3.
(Ders kitabı: Silberschatz Bölüm 8, deadlock avoidance)

Bu modül System'i SADECE OKUR. Testleri elle kurulmuş System'lerle yapabilirsin.
Her process, Process.max_claim ile "her kaynaktan en çok kaç adet isteyeceğini" önceden bildirir.
"""


def compute_need(system):
    def compute_need(system):    need = {}
    for p in system.active_processes():        
        need[p.name] = {}       
        for rname in system.resources:
             kalan_ihtiyac = p.max_claim.get(rname, 0) - p.held.get(rname, 0)           
             need[p.name][rname] = max(0, kalan_ihtiyac)
             return need


def is_safe(system):
    """Güvenlik algoritması (safety algorithm). (True, güvenli_sıra) ya da (False, []) döndürür.

    work = boştaki adetler. Bitmemiş ve need <= work olan İLK process'i (process sırasıyla) bul,
    work += onun tuttukları, güvenli sıraya ekle; her seferinde taramaya baştan başla.
    Herkes bitirildiyse güvenli."""
    # TODO (Üye 3, Sprint 2)
    raise NotImplementedError("is_safe: Üye 3")


def is_request_safe(system, pname, rname, amount=1):
    """Bu istek verilirse sistem güvenli kalır mı? (resource-request algoritması). System DEĞİŞTİRİLMEZ.

      - amount > bildirilen ihtiyaç (need)  ->  ValueError
      - amount > boştaki adet               ->  False (zaten şu an verilemez)
      - değilse: isteği "verilmiş gibi" bir kopyada uygula (copy.deepcopy) ve is_safe'e sor."""
    # TODO (Üye 3, Sprint 2)
    raise NotImplementedError("is_request_safe: Üye 3")


def risk_level(system, deadlocked):
    """(seviye, neden) döndürür. deadlocked = detection.find_deadlocked(system) sonucu (dışarıdan verilir).

    Öncelik sırasıyla ilk uyan:
      CRITICAL: deadlocked boş değil               neden: "Deadlock var: P1, P2"
      HIGH:     is_safe(system) False              neden: güvensiz durum
      MEDIUM:   bekleyen process var YA DA          neden: kimin beklediği / boş kaynak yüzdesi
                boşta kalan toplam adet < %20
      LOW:      diğer her şey                       neden: "Sistem normal"
    Neden metni boş olmamalı ve ilgili process adlarını içermeli."""
    # TODO (Üye 3, Sprint 2)
    raise NotImplementedError("risk_level: Üye 3")
