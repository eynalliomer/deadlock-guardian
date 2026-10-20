"""Testlerde elle System kurmak için yardımcılar. Böylece her üye diğerlerinin kodunu beklemeden test yazabilir."""
from deadlock_guardian.models import WAITING


def hold(system, pname, rname, n=1):
    """pname, rname'den n adet TUTUYOR olsun."""
    p = system.processes[pname]
    p.held[rname] = p.held.get(rname, 0) + n


def wait(system, pname, rname, n=1):
    """pname, rname'den n adet BEKLİYOR olsun (durum WAITING + kuyruğa ekle)."""
    p = system.processes[pname]
    p.state = WAITING
    p.waiting_for[rname] = n
    system.queues.setdefault(rname, []).append(pname)


def claim(system, pname, max_claim):
    """pname'in bildirdiği en çok ihtiyaç (Banker's)."""
    system.processes[pname].max_claim = dict(max_claim)
