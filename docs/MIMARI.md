# Mimari ve Modül Arayüzleri

## Büyük resim

```
                scenarios/*.json
                       |
                 scenario.py        (Üye 1)  JSON -> System
                       |
                       v
   +-------------- models.py ---------------+   ortak veri: Process, Resource, System
   |                   ^                    |
   |                   |                    |
 simulation.py    detection.py          risk.py            recovery.py
  (Üye 1)          (Üye 2)              (Üye 3)             (Üye 4)
  request          wait_for_graph        compute_need        victim_cost
  release          find_cycle            is_safe             choose_victim
  terminate        find_deadlocked       is_request_safe     recover
  değiştirir       sadece okur           risk_level          sim.terminate'i çağırır
                                         sadece okur
                       \                  |                  /
                        +----------- demo.py (Üye 4) -------+
                               printer.py: ekrana yazar
```

## Altın kural: kim neyi değiştirir?

- **Yalnızca `Simulation`** (Üye 1) `System`'i değiştirir: `request`, `release`, `terminate`.
- `detection.py` ve `risk.py` System'i **sadece okur**. Bu yüzden bağımsız test edilirler.
- `recovery.recover` System'i doğrudan değiştirmez; `sim.terminate()` çağırır.
- Herkes yalnızca **kendi dosyasını** düzenler. `models.py`'yi değiştirmek gerekirse önce ekibe sorun.

## Arayüzler (bunlar değişmez, herkes buna güvenir)

| Fonksiyon | Girdi | Çıktı | Sahibi |
|---|---|---|---|
| `Simulation(system)` | `System` | nesne | Üye 1 |
| `sim.request(p, r, adet=1)` | process adı, kaynak adı | `True` (verildi) / `False` (bekliyor) | Üye 1 |
| `sim.release(p, r, adet=1)` | | `None` | Üye 1 |
| `sim.terminate(p)` | | `None` | Üye 1 |
| `wait_for_graph(system)` | `System` | `{"P1": ["P2"], "P2": []}` | Üye 2 |
| `find_cycle(graph)` | graf sözlüğü | döngüdeki düğümler `["P1","P2"]` ya da `None` | Üye 2 |
| `find_deadlocked(system)` | `System` | `["P1","P2"]` (alfabetik, yoksa `[]`) | Üye 2 |
| `compute_need(system)` | `System` | `{"P1": {"R1": 2, "R2": 1}}` | Üye 3 |
| `is_safe(system)` | `System` | `(True, ["P1","P2"])` / `(False, [])` | Üye 3 |
| `is_request_safe(system, p, r, adet)` | | `True` / `False` (aşırı istekte `ValueError`) | Üye 3 |
| `risk_level(system, deadlocked)` | `System`, tespit sonucu | `("HIGH", "neden metni")` | Üye 3 |
| `victim_cost(process)` | `Process` | `int` | Üye 4 |
| `choose_victim(system, deadlocked)` | | process adı | Üye 4 |
| `recover(sim)` | `Simulation` | sonlandırılan adlar `["P1"]` | Üye 4 |
| `format_state(system)` | `System` | tablo metni | Üye 4 |

## Veri yapıları (`models.py`)

```python
Process:  name, state (RUNNING|WAITING|TERMINATED), held {"R1": 1}, waiting_for {"R2": 1},
          max_claim {"R1": 2}, priority, victim_count
Resource: name, total
System:   processes {ad: Process}, resources {ad: Resource}, queues {kaynak: [process adları]}, log [metin]
          available(kaynak)  active_processes()  System.create(resources, processes)
```

## Neden bu kadar basit?

Her şey **isimle** (metin) tutulur, nesne referansı yoktur; sözlük ve liste dışında karmaşık yapı yok.
Böylece herkes tüm kodu okuyup anlayabilir. Algoritmalar için ders kitabındaki (Silberschatz, Bölüm 8) sürümler kullanılır.
