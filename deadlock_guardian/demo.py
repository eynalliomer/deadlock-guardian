"""Deadlock Guardian canlı simülasyon ve demo modülü."""

import sys

from .detection import find_deadlocked
from .printer import format_state
from .recovery import recover
from .risk import risk_level
from .scenario import load_scenario
from .simulation import Simulation


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    path = argv[0] if argv else "scenarios/deadlock.json"

    system, steps = load_scenario(path)
    sim = Simulation(system)

    print(
        f"Senaryo: {path} ({len(system.processes)} process, "
        f"{len(system.resources)} kaynak, {len(steps)} adım)"
    )
    print()
    print(format_state(system))

    for process, action, resource, amount in steps:
        if action == "request":
            sim.request(process, resource, amount)
        else:
            sim.release(process, resource, amount)

        deadlock = find_deadlocked(system)
        seviye, neden = risk_level(system, deadlock)
        print(f"\n> {process} {action} {resource}")
        print(format_state(system))
        print(f"RISK: {seviye} {neden}")

        if deadlock:
            kurbanlar = recover(sim)
            print(f"KURTARMA: {', '.join(kurbanlar)} sonlandırıldı")
            print(format_state(system))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())