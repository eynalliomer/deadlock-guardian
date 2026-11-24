# 1. Giriş ve Problem Tanımı; Simülasyon Modülü

Yazar: Ömer (eynalliomer), Üye 1

## 1.1 Problem: Deadlock

Bir işletim sisteminde process'ler çalışmak için kaynaklara (yazıcı, dosya, bellek bölgesi gibi) ihtiyaç duyar.
Bir process ihtiyaç duyduğu kaynak doluysa bekler. Birkaç process birbirinin tuttuğu kaynağı beklerse hiçbiri
ilerleyemez; buna **deadlock** denir. Örnek: P1, R1'i tutup R2'yi beklerken P2, R2'yi tutup R1'i bekliyorsa
ikisi de sonsuza kadar bekler.

Deadlock'un oluşması için dört koşulun aynı anda sağlanması gerekir (Coffman koşulları):
1. Karşılıklı dışlama: bir kaynağı aynı anda tek process kullanır.
2. Tut ve bekle: process bir kaynağı tutarken başkasını bekler.
3. Geri alınamazlık: kaynak, process bırakmadan elinden alınamaz.
4. Döngüsel bekleme: process'ler arasında birbirini bekleyen bir döngü vardır.

Bu koşullardan biri engellenirse deadlock oluşmaz. İşletim sistemleri deadlock ile üç yoldan başa çıkar:
önleme, kaçınma (Banker's algoritması) ve oluşmasına izin verip tespit edip kurtarma.

## 1.2 Projenin amacı

Deadlock Guardian, gerçek bir işletim sistemi değil, kontrollü bir **simülasyondur**: process'ler ve kaynaklar
Python nesneleridir. Proje üç şey yapar:
- **Risk analizi:** sistemin durumunu LOW, MEDIUM, HIGH ve CRITICAL olarak sınıflandırır (Banker's algoritması).
- **Tespit:** bekleme grafı ve çok örnekli kaynaklar için tespit algoritması ile deadlock'taki process'leri bulur.
- **Kurtarma:** maliyeti en düşük process'i sonlandırarak deadlock'u çözer.

Dört kişilik ekip, modülleri ayrı dallarda geliştirdi ve Pull Request ile birleştirdi.

## 1.3 Simülasyon modülü (`deadlock_guardian/simulation.py`)

Simülasyon motoru sistemin durumunu **değiştiren tek modüldür**. Diğer modüller (tespit, risk, kurtarma) yalnızca
okur. Veri `models.py` içindeki `System` nesnesindedir: process'ler, kaynaklar, her kaynak için bekleme kuyruğu
ve olay kaydı (log).

Bir process üç durumdan birinde olur: **RUNNING** (çalışıyor), **WAITING** (kaynak bekliyor) ve
**TERMINATED** (bitti ya da kurtarmada sonlandırıldı).

### request(process, kaynak, adet)
- Önce doğrulama yapılır: bilinmeyen process ya da kaynak, geçersiz adet, sonlandırılmış veya zaten bekleyen
  process'in yeni istek yapması durumunda `ValueError` verilir.
- Boştaki kaynak yeterliyse hemen verilir (durum RUNNING), `True` döner.
- Yetmiyorsa process WAITING olur, o kaynağın kuyruğunun **sonuna** eklenir, `False` döner.

### release(process, kaynak, adet)
- Process tuttuğundan fazlasını bırakamaz (`ValueError`).
- Kaynak bırakılınca kuyruk **baştan** okunur: baştaki process'in isteği karşılanabiliyorsa kaynak verilir ve
  kuyruktan çıkar; karşılanamıyorsa **durulur**. Arkadaki bir process'in isteği sığsa bile sırayı atlayamaz
  (FIFO). Bu kural adaleti sağlar ve bir process'in sürekli geçilip aç kalmasını (starvation) önler.

### terminate(process)
- Process kuyruklardan çıkarılır, tuttuğu her kaynak bırakılır, durumu TERMINATED olur.
- Boşalan kaynaklar kuyruktaki bekleyenlere sırayla verilir. Kurtarma modülü bu fonksiyonu çağırır.

Her olay log'a bir satır olarak yazılır (örnek: `P1 REQUEST R1 x1 -> GRANTED`, `P2 REQUEST R1 x1 -> WAITING`,
`P1 TERMINATED`).

## 1.4 Simülasyon senaryoları

Senaryolar `scenarios/` klasöründe JSON olarak tutulur ve `python -m deadlock_guardian scenarios/<ad>.json`
ile çalıştırılır.

| Senaryo | Gösterdiği |
|---|---|
| `kuyruk.json` | FIFO kuyruk: bir örnek boşalınca baştaki process'e (2 adet ister) yetmez, arkadaki P3'e yetse bile sırayı atlayamaz. |
| `cift_deadlock.json` | İki bağımsız deadlock (P1-P2 ve P3-P4). Kurtarma iki kurban seçer (P1 ve P4), terminate kaynakları kuyruktakilere verir. |

## 1.5 Test

Simülasyon için 16 birim testi (`tests/test_simulation.py`) ve senaryolar için 7 test
(`tests/test_senaryo_simulasyon.py`) vardır. Tüm modülleri birlikte sınayan entegrasyon testleri
`tests/test_entegrasyon.py` içindedir. Testler `python -m pytest -q` ile çalıştırılır.
