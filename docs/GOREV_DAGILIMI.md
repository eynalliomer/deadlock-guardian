# Görev Dağılımı

Herkes **kendi dosyasında** çalışır; böylece Git'te birbirimizin işini bozmayız (çakışma çıkmaz).
Her görevin bitip bitmediğini **kırmızı testler** söyler: ilgili test dosyası yeşile döndüyse iş tamamdır.

| | **Üye 1: Simülasyon** | **Üye 2: Tespit** | **Üye 3: Risk** | **Üye 4: Kurtarma ve Demo** |
|---|---|---|---|---|
| **Ad Soyad** | ______________ | ______________ | ______________ | __Efe Yılmaz____________ |
| **GitHub kullanıcı adı** | ______________ | ______________ | ____________ | _________bahadir-e_____ |
| **Dosyaları** | `simulation.py`, `scenario.py`, `models.py` | `detection.py` | `risk.py` | `recovery.py`, `printer.py`, `demo.py` |
| **Test dosyası** | `test_simulation.py` | `test_detection.py` | `test_risk.py` | `test_recovery.py`, `test_printer_demo.py` |
| **Ders konusu** | Process durumları, kaynak tahsisi, bekleme kuyruğu | Resource Allocation Graph, döngü, deadlock detection | Güvenli durum, Banker's Algorithm, risk | Deadlock recovery, kurban seçimi |

## Dallar

| Üye | Dal |
|---|---|
| Üye 1 | `uye1-simulasyon` |
| Üye 2 | `uye2-tespit` |
| Üye 3 | `uye3-risk` |
| Üye 4 | `uye4-kurtarma-demo` |

## Sprint 1: ara görüşme (21 Ekim, Çarşamba)

Hedef: her üye **kendi ilk küçük fonksiyonunu** yazıp test eder ve push'lar. Her biri 30-60 dakikalık iş.

| Üye | Sprint 1 görevi | Eklenecek test | Yapıldı mı? |
|---|---|---|---|
| Ortak | İskelet: veri yapıları (`models.py`), senaryo okuma, ekran çıktısı, demo | `test_models`, `test_scenario`, `test_printer_demo` (13 test) | ☑ hazır |
| Üye 1 | `Simulation.request`: boş kaynağı verme | `test_bos_kaynak_hemen_verilir` | ☐ |
| Üye 2 | `wait_for_graph`: bekleme grafı | `test_wait_for_graph_*` (4 test) | ☐ |
| Üye 3 | `compute_need`: Need = Max − Held | `test_compute_need*` (3 test) | ☐ |
| Üye 4 | `victim_cost`: kurban maliyeti | `test_victim_cost_*` (3 test) | ☐ |


## Sprint 2: bir sonraki ara teslim

| Üye | Teslim edeceği modül | Tamamlanınca geçecek testler |
|---|---|---|
| Üye 1 | `request` (bekletme, kuyruk, hatalar, log), `release`, `terminate` | `test_simulation.py` (16 test) |
| Üye 2 | `find_cycle` (DFS), `find_deadlocked` (çok örnekli kaynaklar) | `test_detection.py` (14 test) |
| Üye 3 | `is_safe`, `is_request_safe`, `risk_level` | `test_risk.py` (15 test) |
| Üye 4 | `choose_victim`, `recover`, demonun adım adım çalışması | `test_recovery.py` (9 test) |

## Final

- Entegrasyon testi (`tests/test_senaryolar.py`) eklenir ve geçer (tüm modüller birlikte).
- Ek senaryolar, rapor ve sunum. Ayrıntı için GitHub'daki **Final** issue'ları.
