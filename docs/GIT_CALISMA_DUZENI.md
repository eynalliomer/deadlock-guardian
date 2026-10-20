# Git Çalışma Düzeni (4 kişi, tek depo)

**Kural 1:** Herkesin **kendi dalı** vardır; kimse doğrudan `main`'e yazmaz.
**Kural 2:** Sprint sonunda dal, **Pull Request (PR)** ile `main`'e katılır; PR'ı **başka bir üye** okuyup onaylar.
**Kural 3:** Herkes yalnızca **kendi dosyalarında** çalışır (`docs/MIMARI.md`'ye bak). Çakışma olmaz.

| Üye | Dal | Dosyaları |
|---|---|---|
| Üye 1 | `uye1-simulasyon` | `simulation.py` |
| Üye 2 | `uye2-tespit` | `detection.py` |
| Üye 3 | `uye3-risk` | `risk.py` |
| Üye 4 | `uye4-kurtarma-demo` | `recovery.py`, `demo.py` |

## Bir kez: depoyu indir ve kendi dalına geç

```bash
git clone https://github.com/eynalliomer/deadlock-guardian.git
cd deadlock-guardian
python3 -m venv .venv && source .venv/bin/activate    # Windows: py -m venv .venv ; .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q                                    # ortak testler geçer
git switch uye2-tespit                                 # kendi dalın (adını tablodan bak)
```

## Her çalışmada

```bash
git switch uye2-tespit
git pull origin main                  # main'e giren yeni işleri kendi dalına al
# ... kodu yaz, kendi test dosyanı ekle ...
python -m pytest -q                   # testler
git add deadlock_guardian/detection.py tests/test_detection.py
git commit -m "wait_for_graph yazıldı"
git push                              # ilk seferde: git push -u origin uye2-tespit
```

Küçük ve sık commit at; mesaj ne yaptığını söylesin (Türkçe, kısa).

## Sprint sonunda: Pull Request

1. GitHub'da depoya gir; **Compare & pull request** düğmesine bas.
2. Açıklamaya `Closes #<issue no>` yaz, sağdan bir arkadaşını **Reviewer** seç, **Create pull request**.
3. İncelemeci **Files changed** sekmesinde kodu okur, yerelde dener (`git fetch`, `git switch <dal>`, `python -m pytest -q`) ve **Approve** eder.
4. **Merge pull request** (normal merge, squash değil) ve **Confirm**. Dal silinmez; çalışmaya devam edilir.
5. Kendi bilgisayarında: `git switch main`, `git pull`, sonra kendi dalına dön ve `git pull origin main`.

## Sık sorunlar

| Sorun | Çözüm |
|---|---|
| `git push` reddedildi | Önce `git pull origin main`, sonra tekrar `git push`. |
| Yanlış dalda çalıştım | `git status` hangi dalda olduğunu gösterir; commit atmadan önce hep bak. |
| Merge conflict | Dosyayı aç, `<<<<<<<` işaretli yeri elle düzelt, `git add` ve `git commit`. Kendi dosyanda kaldıkça neredeyse hiç olmaz. |
