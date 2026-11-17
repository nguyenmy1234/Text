# 02_Text — Phân loại cảm xúc đánh giá sản phẩm Amazon

**Bài tập lớn — Nền tảng lập trình cho phân tích và trực quan dữ liệu (CO5177), HK 261, 2026–2027.**
Giảng viên: Lê Thành Sách · Sinh viên: Nguyễn Thị Hồng Hạnh – 2470316 (theo `index.html`)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nguyenmy1234/text/blob/main/02_Text/notebooks/02_Text_Amazon_Reviews.ipynb)

Dự đoán đánh giá Amazon (tiếng Anh) là **Tiêu cực / Trung tính / Tích cực**. Hai câu hỏi của bài:
(1) từ nào phân biệt ba lớp; (2) dữ liệu mất cân bằng (~90% tích cực) ảnh hưởng thế nào và xử lý mất cân bằng bắt thêm được bao nhiêu đánh giá tiêu cực/trung tính.

## Cấu trúc thư mục

```
02_Text/
├── data/
│   └── text/
│       └── README.md
├── notebooks/
│   └── 02_Text_Amazon_Reviews.ipynb
├── report/
│   └── BAO_CAO_TONG_HOP.md
├── scripts/
│   └── prepare_amazon_dataset.py
├── .gitignore
├── index.html
├── README.md
├── requirements.txt
└── UPLOAD_GITHUB.md
```

`data/text/amazon_reviews.csv` và `external_test.jsonl` chưa có trong cây này: bạn thêm vào `data/text/` trước khi push (xem `data/text/README.md`). Cách upload một lần: `UPLOAD_GITHUB.md`.

## Cách chạy

**Google Colab (khuyến nghị):** bấm nút *Open In Colab* ở trên (sau khi đã push thư mục này lên GitHub) → *Runtime → Run all*.
Ô tải dữ liệu tự tìm file theo thứ tự: thư mục cục bộ → GitHub → hộp thoại **Choose files** để upload `amazon_reviews.csv` (và `external_test.jsonl` nếu có).
Colab đã có sẵn mọi thư viện cần dùng; ô đầu tiên tự cài thêm nếu thiếu.

**Máy cá nhân:**
```bash
pip install -r requirements.txt
python scripts/prepare_amazon_dataset.py      # kiểm tra dữ liệu
jupyter notebook notebooks/02_Text_Amazon_Reviews.ipynb
```

Mục 4.6 (so sánh RoBERTa zero-shot, tải ~500 MB) là tùy chọn: thiếu `torch`/`transformers` hoặc không có mạng thì tự bỏ qua. Đặt `RUN_TRANSFORMER = False` nếu muốn tắt hẳn.

## Kết quả chính (tập Test 737 mẫu, dùng một lần)

| Mô hình | Accuracy | F1 macro | ROC-AUC | Bắt Tiêu cực | Bắt Trung tính |
|---|---|---|---|---|---|
| Dummy (lớp đa số) | 0.905 | 0.317 | 0.500 | 0/48 | 0/22 |
| LogReg mặc định (baseline) | 0.923 | 0.458 | 0.907 | 13/48 | 0/22 |
| **LogReg tuned (mô hình cuối)** | 0.919 | **0.593** | 0.884 | 37/48 | 3/22 |

Mô hình cuối: TF-IDF 5.000 đặc trưng (1–2-gram) + Logistic Regression `C=3`, `class_weight='balanced'`, chọn theo F1 macro trên Validation.
Trên tập ngoài (5.000 đánh giá nhiều ngành hàng) F1 macro giảm còn **0.389**: mô hình học từ vựng thẻ nhớ nên khó tổng quát hóa.
Chi tiết đầy đủ ở `report/BAO_CAO_TONG_HOP.md`.

## Tái lập
`random_state = 42` ở mọi bước chia tập, cross-validation và mô hình. Mọi bước học tham số từ dữ liệu (TF-IDF, scaler, imputer) nằm trong `Pipeline` và chỉ `fit` trên Train để tránh rò rỉ dữ liệu.
