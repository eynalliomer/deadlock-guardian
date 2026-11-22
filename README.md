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

## Şu an ne çalışıyor? (Sprint 2)

`python -m deadlock_guardian scenarios/deadlock.json` senaryoyu adım adım çalıştırır. Her adımdan sonra
sistemin durumunu ve risk seviyesini (LOW / MEDIUM / HIGH / CRITICAL) yazar. Deadlock oluşunca bunu tespit
eder, kurban process'i seçip sonlandırır ve sistemi kurtarır. `scenarios/normal.json` deadlock'suz bir akış gösterir.
`python -m pytest -q` tüm modüllerin birim testlerini çalıştırır.

## Modüller

| Modül | Ne yapar? | Sahibi | Durum |
|---|---|---|---|
| `models.py`, `scenario.py` | Ortak veri yapıları, senaryo okuma | Ömer Faruk Eynallı | ✅ |
| `simulation.py` | request / release / bekleme kuyruğu / terminate | Ömer Faruk Eynallı | ✅ |
| `detection.py` | Bekleme grafı, döngü, deadlock tespiti | Selma Süeda Özçallı | ✅ |
| `risk.py` | Banker's Algorithm, risk seviyeleri | Meri Lara Elesho | ✅ |
| `recovery.py`, `printer.py`, `demo.py` | Kurban seçimi, kurtarma, ekran çıktısı, demo | Bahadır Efe Yılmaz | ✅ |

Her üyenin kendi dalı vardır: `eynalliomer-simulasyon`, `selmaozc-tespit`, `laraelesho-risk`, `bahadir-e-kurtarma-demo`.

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
