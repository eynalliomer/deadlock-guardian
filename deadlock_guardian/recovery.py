from .detection import find_deadlocked


def victim_cost(process):
    """Bir process'in feda edilme maliyetini hesaplar."""
    toplam = sum(process.held.values())
    return process.priority * 10 - 2 * toplam + 5 * process.victim_count


def choose_victim(system, deadlocked):
    
    if not deadlocked:
        raise ValueError("deadlock listesi bos")

    en_iyi = None
    en_dusuk = None

    for ad in sorted(deadlocked):  # alfabetik bak: eşitlikte ilk gelen kalır
        maliyet = victim_cost(system.processes[ad])
        if en_dusuk is None or maliyet < en_dusuk:
            en_dusuk = maliyet
            en_iyi = ad

    return en_iyi


def recover(sim):
   
    kurbanlar = []

    while True:
        deadlock = find_deadlocked(sim.system)
        if not deadlock:
            return kurbanlar

        kurban = choose_victim(sim.system, deadlock)
        sim.system.processes[kurban].victim_count += 1
        sim.terminate(kurban)
        kurbanlar.append(kurban)