"""Ortak veri yapıları. Projedeki herkes bunları kullanır.

Sahibi: Üye 1. Bir alanı değiştirmek/eklemek gerekirse önce ekibe haber ver,
çünkü tespit, risk ve kurtarma modülleri bu yapılara güveniyor.

Basit tutmak için her şey isimle (metin) tutulur: "P1", "R1". Nesne referansı yok.
"""
from dataclasses import dataclass, field

# Bir process'in alabileceği durumlar
RUNNING = "RUNNING"        # ilerleyebiliyor
WAITING = "WAITING"        # bir kaynağı bekliyor
TERMINATED = "TERMINATED"  # bitti ya da recovery ile sonlandırıldı


@dataclass
class Process:
    name: str
    state: str = RUNNING
    held: dict = field(default_factory=dict)         # tuttuğu kaynaklar     {"R1": 1}
    waiting_for: dict = field(default_factory=dict)  # beklediği kaynaklar   {"R2": 1}  (boş = bir şey beklemiyor)
    max_claim: dict = field(default_factory=dict)    # Banker's için bildirdiği en çok ihtiyaç {"R1": 2}
    priority: int = 1                                # recovery: büyük sayı = daha önemli process
    victim_count: int = 0                            # recovery: kaç kez kurban seçildi


@dataclass
class Resource:
    name: str
    total: int = 1  # bu kaynaktan toplam kaç örnek (adet) var


@dataclass
class System:
    """Sistemin o anki tam fotoğrafı."""
    processes: dict = field(default_factory=dict)  # {"P1": Process(...)}
    resources: dict = field(default_factory=dict)  # {"R1": Resource(...)}
    queues: dict = field(default_factory=dict)     # {"R1": ["P2", "P3"]}  bekleme sırası (önce gelen önce alır)
    log: list = field(default_factory=list)        # olay kaydı, her satır bir metin

    @classmethod
    def create(cls, resources, processes):
        """System.create({"R1": 1, "R2": 2}, ["P1", "P2"])  ->  2 kaynak, 2 process."""
        return cls(
            processes={n: Process(n) for n in processes},
            resources={n: Resource(n, total) for n, total in resources.items()},
            queues={n: [] for n in resources},
        )

    def available(self, rname):
        """Bu kaynaktan şu an boşta kaç örnek var? (toplam - tutulan)"""
        held = sum(p.held.get(rname, 0) for p in self.processes.values())
        return self.resources[rname].total - held

    def active_processes(self):
        """Sonlandırılmamış process'ler (eklenme sırasıyla)."""
        return [p for p in self.processes.values() if p.state != TERMINATED]
