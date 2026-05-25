# AIGrep - AI Destekli Kod Operasyon Aracı

AIGrep, belirlediğiniz arama desenine göre projede hızlı bir şekilde dosya taraması yapmanızı ve sonuçları ekranda görüntülemenizi sağlayan, PyQt5 tabanlı bir masaüstü uygulamasıdır.

> Not: Mevcut sürümde arama işlemi `aigrep_core.py` içindeki fonksiyonla yapılır. GUI’de görünen ripgrep (`rg`) komutu bilgilendirme amaçlı üretilir; gerçek arama `arama_yap()` tarafından gerçekleştirilir.

---

## Özellikler
- Proje klasöründe dosya taraması
- Regex tabanlı arama deseni
- Dosya uzantısına göre filtreleme (`py`, `txt` vb.)
- Sonuçların satır numarası ile listelenmesi
- `analysis.json` dosyasına sonuçların kaydedilmesi (AI ile analiz butonu)

---

## Gereksinimler
- Python 3.x
- PyQt5

---

## Kurulum
Aşağıdaki komutla bağımlılıkları yükleyebilirsiniz:

```bash
pip install PyQt5
```

> Eğer sisteminizde `pip` yoksa veya Python sürümünüz uyumsuzsa, önce Python kurulumu yapmanız gerekebilir.

---

## Çalıştırma
Proje klasöründe şu komutu çalıştırın:

```bash
python main.py
```

---

## Kullanım
Uygulama açıldığında:

1. **Arama deseni**: Örneğin `def` veya regex bir ifade yazın.
2. **Klasör yolu**: Tarama yapılacak klasörü girin (örn. `.`).
3. **Dosya tipi**: Aranacak dosya uzantısını girin (örn. `py`).
4. (Opsiyonel) **Bayraklar**: GUI’de işaretlenebilen bayraklar görüntülenir; ancak mevcut çekirdek arama mantığında doğrudan kullanılmıyor.
5. **▶ Arama Yap**: Eşleşmeleri ekranda görüntüler.
6. **✨ AI ile Analiz Et**: Sonuçları `analysis.json` dosyasına yazar.

---

## Teknik Detaylar
### `aigrep_core.py`
- `process_file(...)`: Tek tek dosyalarda regex eşleşmelerini arar.
- `arama_yap(pattern, search_path, replace_text=None, ext_list=['.py'])`:
  - Belirtilen dizin altında `ext_list` ile uyumlu dosyaları dolaşır.
  - Paralel işleme (ThreadPoolExecutor) ile aramayı hızlandırır.
  - Sonuçları şu formatta döndürür:
    - `file`: Dosya yolu
    - `line_number`: Satır numarası
    - `original_content`: Satır içeriği

### `main.py`
- `PyQt5` ile grafik arayüz oluşturur.
- Kullanıcı girdilerine göre arama desenini ve hedef uzantıyı belirler.
- Arama çıktısını `QTextEdit` üzerinde listeler.

---

## Çıktılar
- Arama sonuçları uygulama ekranında görünür.
- “AI ile Analiz Et” ile birlikte `analysis.json` oluşturulur.

---

## Geliştirme Notları (İyileştirme Fikirleri)
- GUI’deki bayrakları (`-i`, `-n`, `-w` vb.) gerçek aramaya entegre etmek.
- Sonuçlarda satır içeriği yerine bağlam (önce/sonra satırlar) göstermek.
- `analysis.json` için kullanıcıya seçilebilir çıktı yolu sunmak.

