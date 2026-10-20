# Deadlock Guardian

İşletim Sistemleri (BİM 361) dönem projesi. Process'ler kaynak ister, bırakır, bekler. Sistem
**deadlock riskini ölçer**, **deadlock'u tespit eder** ve **kurban process seçerek sistemi kurtarır**.

Gerçek işletim sistemini değil, kontrollü bir **simülasyonu** yönetir. Python standart kütüphanesi dışında
bir şey gerekmez (testler için `pytest`).

## Nasıl kurulur ve çalıştırılır?

Python **yorumlanan** bir dildir, derleme adımı yoktur. Python 3.10 veya üstü gerekir.

```bash
git clone <depo-adresi>
cd deadlock-guardian

python3 -m venv .venv                 # sanal ortam (Windows: py -m venv .venv)
source .venv/bin/activate             # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m deadlock_guardian scenarios/deadlock.json    # demo
python -m pytest -q                                    # testler
```

Windows'ta `python3` yerine `py` yazın.

## Şu an ne çalışıyor? (Sprint 1)

`python -m deadlock_guardian scenarios/deadlock.json` komutu senaryo dosyasını **okuyup belleğe alır**
(2 process, 2 kaynak, 4 adım) ve başlangıç durumunu tablo olarak yazar. Ardından modüller sırayla dolacak.
`python -m pytest -q` ortak kısımların testlerini çalıştırır. Her modülün testi, o modül yazılırken
`tests/` altına eklenir; depo üyeler commit attıkça dolar.

## Modüller

| Modül | Ne yapar? | Sahibi | Durum |
|---|---|---|---|
| `models.py`, `scenario.py` | Ortak veri yapıları, senaryo okuma | Üye 1 | ✅ iskelet hazır |
| `simulation.py` | request / release / bekleme kuyruğu / terminate | Üye 1 | ⏳ |
| `detection.py` | Bekleme grafı, döngü, deadlock tespiti | Üye 2 | ⏳ |
| `risk.py` | Banker's Algorithm, risk seviyeleri | Üye 3 | ⏳ |
| `recovery.py`, `printer.py`, `demo.py` | Kurban seçimi, kurtarma, ekran çıktısı, demo | Üye 4 | ⏳ (printer ✅) |

Her üyenin kendi dalı vardır: `uye1-simulasyon`, `uye2-tespit`, `uye3-risk`, `uye4-kurtarma-demo`.

Ayrıntılar: [Görev dağılımı](docs/GOREV_DAGILIMI.md) · [Mimari ve arayüzler](docs/MIMARI.md) ·
[Git çalışma düzeni](docs/GIT_CALISMA_DUZENI.md)

## Klasör yapısı

```
deadlock_guardian/   kaynak kod (her modül ayrı dosya)
tests/               pytest testleri (her modülün kendi test dosyası)
scenarios/           JSON senaryolar (normal.json, deadlock.json)
docs/                görev dağılımı, mimari, git çalışma düzeni
```

## Kaynak

Silberschatz, Galvin, Gagne: *Operating System Concepts*, Bölüm 8 (Deadlocks).
