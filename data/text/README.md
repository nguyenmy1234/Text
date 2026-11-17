# Thư mục dữ liệu

Đặt hai file sau vào **thư mục này** (`02_Text/data/text/`) trước khi chạy notebook:

| File | Bắt buộc | Nội dung |
|---|---|---|
| `amazon_reviews.csv` | Có | 4.915 đánh giá × 12 cột: `Unnamed: 0, reviewerName, overall, reviewText, reviewTime, day_diff, helpful_yes, helpful_no, total_vote, score_pos_neg_diff, score_average_rating, wilson_lower_bound` |
| `external_test.jsonl` | Không | 5.000 dòng JSON, mỗi dòng có `text` và `label` (0–4, tương ứng 1–5 sao). Thiếu file này thì chỉ mục 4.5 của notebook bị bỏ qua. |

Kiểm tra nhanh file đã đúng định dạng chưa: `python scripts/prepare_amazon_dataset.py`

Nếu push lên GitHub, hãy push cả hai file này để notebook trên Colab tự tải được.
