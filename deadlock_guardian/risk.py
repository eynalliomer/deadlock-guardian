"""Risk analizi: Banker's Algorithm ve risk seviyeleri.  SAHİBİ: ÜYE 3.
(Ders kitabı: Silberschatz Bölüm 8, deadlock avoidance)

Bu modül System'i SADECE OKUR. Testleri elle kurulmuş System'lerle yapabilirsin.
Her process, Process.max_claim ile "her kaynaktan en çok kaç adet isteyeceğini" önceden bildirir.
"""
import copy

def compute_need(system):   
    need = {}
    for p in system.active_processes():        
        need[p.name] = {}       
        for rname in system.resources:
             kalan_ihtiyac = p.max_claim.get(rname, 0) - p.held.get(rname, 0)           
             need[p.name][rname] = max(0, kalan_ihtiyac)
    return need

def yetiyor(need_p, work):
    """Bu process'in kalan ihtiyacı, boştaki kaynaklara (work) yetiyor mu?"""
    for rname in need_p:
        if need_p[rname] > work[rname]:
            return False
    return True            

 
def is_safe(system):
    """Güvenlik algoritması (safety algorithm). (True, güvenli_sıra) ya da (False, []) döndürür.

    work = boştaki adetler. Bitmemiş ve need <= work olan İLK process'i (process sırasıyla) bul,
    work += onun tuttukları, güvenli sıraya ekle; her seferinde taramaya baştan başla.
    Herkes bitirildiyse güvenli."""
    need = compute_need(system)
    work = {}
    for rname in system.resources:
        work[rname] = system.available(rname)
    kalan = list(system.active_processes())
    sira = []
    while kalan:
        bulundu = None
        for p in kalan:
            if yetiyor(need[p.name], work):
                bulundu = p
                break
        if bulundu is None:  # kimse bitiremiyor: güvensiz
            return False, []
        for rname, adet in bulundu.held.items():
            work[rname] = work[rname] + adet  # bitince tuttuklarını geri verir
        sira.append(bulundu.name)
        kalan.remove(bulundu)
    return True, sira



def is_request_safe(system, pname, rname, amount=1):
    """Bu istek verilirse sistem güvenli kalır mı? (resource-request algoritması). System DEĞİŞTİRİLMEZ.

      - amount > bildirilen ihtiyaç (need)  ->  ValueError
      - amount > boştaki adet               ->  False (zaten şu an verilemez)
      - değilse: isteği "verilmiş gibi" bir kopyada uygula (copy.deepcopy) ve is_safe'e sor."""
    if amount > compute_need(system)[pname][rname]:
        raise ValueError(f"{pname} bildirdiğinden fazla istiyor")
    if amount > system.available(rname):
        return False
    kopya = copy.deepcopy(system)  # gerçek sistemi bozmamak için kopya
    p = kopya.processes[pname]
    p.held[rname] = p.held.get(rname, 0) + amount
    guvenli, sira = is_safe(kopya)
    return guvenli
   
def risk_level(system, deadlocked):
    """(seviye, neden) döndürür. deadlocked = detection.find_deadlocked(system) sonucu (dışarıdan verilir).

    Öncelik sırasıyla ilk uyan:
      CRITICAL: deadlocked boş değil               neden: "Deadlock var: P1, P2"
      HIGH:     is_safe(system) False              neden: güvensiz durum
      MEDIUM:   bekleyen process var YA DA          neden: kimin beklediği / boş kaynak yüzdesi
                boşta kalan toplam adet < %20
      LOW:      diğer her şey                       neden: "Sistem normal"
    Neden metni boş olmamalı ve ilgili process adlarını içermeli."""
    if deadlocked:
        return "CRITICAL", "Deadlock var: " + ", ".join(deadlocked)
    guvenli, sira = is_safe(system)
    if not guvenli:
        return "HIGH", "Sistem güvensiz durumda: güvenli bir bitirme sırası yok"
    
    bekleyenler = []
    for p in system.active_processes():
        if p.waiting_for:
            bekleyenler.append(p.name)
    if bekleyenler:
        return "MEDIUM", "Bekleyen process var: " + ", ".join(bekleyenler)
        
    toplam = 0
    bos = 0
    for rname in system.resources:
        toplam = toplam + system.resources[rname].total
        bos = bos + system.available(rname)
    if toplam > 0 and bos / toplam < 0.2:
        return "MEDIUM", f"Boş kaynak az: %{bos * 100 // toplam}"
    
    return "LOW", "Sistem normal"