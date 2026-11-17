# Đưa cả thư mục lên GitHub một lần

Repo đích (theo README): `nguyenmy1234/text`, thư mục con `02_Text/`. Trước khi upload, đặt `amazon_reviews.csv` (và `external_test.jsonl`) vào `data/text/`.

## Cách 1: kéo thả trên web (không cần cài git)
1. Vào repo → **Add file → Upload files**.
2. Kéo **cả thư mục `02_Text`** vào khung (giữ nguyên cấu trúc con). Mỗi file phải nhỏ hơn 25 MB.
3. Ghi commit message, ví dụ `Add 02_Text: Amazon sentiment`, bấm **Commit changes**.

## Cách 2: dòng lệnh (một lần)
```bash
git clone https://github.com/nguyenmy1234/text.git
cd text
# chép thư mục 02_Text (đã có data/text/*.csv, *.jsonl) vào đây
git add 02_Text
git commit -m "Add 02_Text: Amazon sentiment"
git push origin main
```

## Sau khi upload
- Mở `https://github.com/nguyenmy1234/text/blob/main/02_Text/notebooks/02_Text_Amazon_Reviews.ipynb` rồi chọn *Open in Colab*, hoặc dùng nút trong `README.md`.
- Bật **Settings → Pages** (branch `main`, thư mục `/ (root)`) nếu muốn xem `index.html` như một trang web: `https://nguyenmy1234.github.io/text/02_Text/index.html`.
- Nếu `data/text/` đã nằm trên GitHub, notebook trên Colab tự tải dữ liệu, không cần upload tay.
