"""Senaryo dosyasını (JSON) okuyup bellekte bir System kurar.

Sahibi: Üye 1. Girdi dosyasının okunup hafızaya alınması ara teslimin mini demosudur.

Dosya biçimi (scenarios/deadlock.json'a bak):
{
  "resources": {"R1": 1, "R2": 1},
  "processes": {"P1": {"priority": 1, "max": {"R1": 1, "R2": 1}}, "P2": {}},
  "steps": [["P1", "request", "R1"], ["P1", "release", "R1", 1]]   # 4. eleman (adet) isteğe bağlı
}
"""
import json

ACTIONS = ("request", "release")


def load_scenario(path):
    """JSON dosyasını okur, (System, steps) döndürür. steps = [(process, action, resource, adet), ...]"""
    from .models import Process, Resource, System

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for key in ("resources", "processes", "steps"):
        if key not in data:
            raise ValueError(f"Senaryoda '{key}' bölümü yok: {path}")

    system = System(
        resources={n: Resource(n, total) for n, total in data["resources"].items()},
        queues={n: [] for n in data["resources"]},
    )
    for name, info in data["processes"].items():
        system.processes[name] = Process(
            name, priority=info.get("priority", 1), max_claim=dict(info.get("max", {}))
        )

    steps = []
    for raw in data["steps"]:
        process, action, resource = raw[0], raw[1], raw[2]
        amount = raw[3] if len(raw) > 3 else 1
        if action not in ACTIONS:
            raise ValueError(f"Bilinmeyen işlem '{action}' (geçerli: {ACTIONS})")
        if process not in system.processes or resource not in system.resources:
            raise ValueError(f"Senaryo adımında bilinmeyen isim: {raw}")
        steps.append((process, action, resource, amount))
    return system, steps
