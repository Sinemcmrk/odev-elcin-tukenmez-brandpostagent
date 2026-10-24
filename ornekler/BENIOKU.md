# Örnek çıktılar

**Agent örnekleri** bu klasöre `ornekler_uret.bat` çalıştırıldığında eklenir. Her marka için 4 Instagram Feed ve 1 Instagram Story
(toplam 20 örnek) üretilir; Feed tasarımlarını Agent 1 otomatik ve birbirinden farklı kompozisyonlarda seçer. Her örnekte Agent 1 planı ekrana yazar; **siz onaylarsınız** (ya da geri bildirim verirsiniz),
sonra Agent 2 PNG'yi üretir. Her örnek klasöründe şunlar bulunur:

- `*.png`: görseller (Feed 1080×1350, Story 1080×1920; carousel'de tüm sayfalar)
- `caption.txt`: caption ve hashtag'ler
- `plan_onayli.json`: Agent 1'in planı ve onay kaydı (iki aşama arasındaki JSON)
- `post.json`: Agent 2'nin üretim kaydı

Ayrıca `OZET.md` (tüm caption'lar, kompozisyonlar ve kararlar) ve `ozet.png` (her markanın örnekleri yan yana, karşılaştırma görseli) oluşur.
