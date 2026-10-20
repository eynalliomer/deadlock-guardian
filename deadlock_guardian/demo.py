"""Komut satırı demosu.  Çalıştır:  python -m deadlock_guardian scenarios/deadlock.json

Sahibi: Üye 4.
Şu an (Sprint 1): senaryoyu okuyup başlangıç durumunu yazar. Bu, "girdi dosyasının okunup
hafızaya alınması" mini demosudur.
"""
import sys

from .printer import format_state
from .scenario import load_scenario


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else "scenarios/deadlock.json"
    system, steps = load_scenario(path)
    print(f"Senaryo: {path}  ({len(system.processes)} process, {len(system.resources)} kaynak, {len(steps)} adım)")
    print()
    print(format_state(system))

    # TODO (Üye 4, Sprint 2): steps listesini Simulation ile adım adım çalıştır;
    #   her adımdan sonra durum tablosunu, risk seviyesini (risk.risk_level) ve
    #   deadlock'u (detection.find_deadlocked) yazdır. Deadlock varsa recovery.recover çağır.
    return 0
