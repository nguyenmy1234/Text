# Báo cáo tổng hợp — Bài 2 (Text): Phân loại cảm xúc đánh giá sản phẩm Amazon

Môn: Nền tảng lập trình cho phân tích và trực quan dữ liệu (CO5177) · HK 261, 2026–2027 · GV: Lê Thành Sách
Mọi số liệu dưới đây lấy từ **output đã chạy của notebook** `notebooks/02_Text_Amazon_Reviews.ipynb`. Nếu chạy lại với dữ liệu thật, các số phải khớp.

## 1. Bài toán và dữ liệu
- Phân loại đa lớp 3 lớp từ nội dung đánh giá. Nhãn suy ra từ điểm sao: 1–2 sao → Tiêu cực (0), 3 sao → Trung tính (1), 4–5 sao → Tích cực (2).
- Dữ liệu: `amazon_reviews.csv`, **4.915 dòng × 12 cột**, chủ yếu là đánh giá thẻ nhớ SD/microSD (01/2012–12/2014). Nhãn lấy từ điểm sao nên có nhiễu.
- Làm sạch: xóa **1** dòng thiếu `reviewText`, xóa **2** dòng trùng nội dung → còn **4.912** đánh giá.
- Phân bố nhãn: Tích cực **4.446 (90,5%)**, Tiêu cực **324 (6,6%)**, Trung tính **142 (2,9%)**; tỉ lệ lớp đa số / thiểu số = **31,3 : 1**.
- Chia **70 / 15 / 15** có phân tầng (Train 3.438, Validation 737, Test 737), `random_state=42`.

## 2. Khám phá dữ liệu (EDA)
- Độ dài đánh giá lệch phải mạnh (skewness 8,48; trung bình 50 từ, dài nhất 1.554 từ). Đánh giá **tiêu cực dài hơn**: trung bình 106,5 từ (median 78), Trung tính 7[...]
- Tỉ lệ tiêu cực giảm theo năm đăng: 12,4% (2012), 7,3% (2013), 3,9% (2014). Đánh giá tiêu cực nhận nhiều bình chọn hơn: 7,96 phiếu/đánh giá so với 1,08 (Tích c��[...]
- Tương quan Spearman: `word_count` và `char_count` gần trùng nhau (ρ = 0,979); `overall` chỉ tương quan yếu với các cột số (|ρ| ≤ 0,256) → thông tin chính nằm trong v[...]
- Ngoại lai (IQR): các cột đếm có nhiều giá trị ngoại lai (ví dụ `word_count` 9,2%) nhưng là giá trị thật nên **không xóa**, nén bằng `log1p`.
- Bằng chứng miền sản phẩm: 51,5% đánh giá nhắc "card/cards", 76,4% nhắc ít nhất một từ khóa thẻ nhớ.

## 3. Tiền xử lý (trong `Pipeline`, chống rò rỉ dữ liệu)
- Lớp `TextCleaner`: chữ thường, bỏ HTML/URL, mở rộng dạng viết tắt phủ định (`don't` → `do not`), chỉ giữ chữ cái, loại stop words **nhưng giữ từ phủ đ�[...]
- TF-IDF: `max_features=5000`, `ngram_range=(1, 2)`, `min_df=2`, `sublinear_tf=True`.
- Thử thêm 8 đặc trưng số (meta-features) với `log1p` + `StandardScaler`; kết quả ở mục 5.

## 4. Thước đo và so sánh mô hình (Validation, 737 mẫu)
Thước đo chính là **F1 macro** (Accuracy gây hiểu nhầm vì ~90% là lớp Tích cực).

| Mô hình | Accuracy | Precision | Recall | F1 macro | ROC-AUC | F1 Trung tính |
|---|---|---|---|---|---|---|
| Dummy (lớp đa số) | 0.905 | 0.302 | 0.333 | 0.317 | 0.500 | 0.000 |
| MultinomialNB | 0.905 | 0.302 | 0.333 | 0.317 | 0.830 | 0.000 |
| MultinomialNB + balanced | 0.919 | 0.517 | 0.452 | 0.473 | 0.824 | 0.000 |
| LogisticRegression | 0.925 | 0.603 | 0.435 | 0.472 | 0.898 | 0.000 |
| LogisticRegression + balanced | 0.910 | 0.574 | 0.636 | 0.599 | 0.877 | 0.195 |
| LinearSVC | 0.932 | 0.569 | 0.488 | 0.516 | 0.876 | 0.000 |
| LinearSVC + balanced | 0.932 | 0.622 | 0.535 | 0.560 | 0.875 | 0.077 |

Xử lý mất cân bằng tăng F1 macro ở cả ba thuật toán (NB 0,317 → 0,473; LogReg 0,472 → 0,599; LinearSVC 0,516 → 0,560).

## 5. Tinh chỉnh và chọn mô hình
- `GridSearchCV`, 5-fold phân tầng trên Train, tiêu chí F1 macro. Tham số tốt nhất: MultinomialNB `alpha=0.05, fit_prior=False`; LogReg `C=3, class_weight='balanced'`; LinearSVC `C=1, [...]`
- Validation sau tuning (F1 macro): **LogReg 0.620** > LinearSVC 0.560 > MultinomialNB 0.527.
- Meta-features **không giúp**: LogReg 0.620 → 0.619; LinearSVC 0.560 → 0.543.
- Mô hình cuối chọn theo Validation: **LogisticRegression (tuned), chỉ TF-IDF**.

## 6. Kết quả trên tập Test (737 mẫu, dùng một lần)

| Mô hình | Accuracy | Precision | Recall | F1 macro | ROC-AUC | F1 Trung tính |
|---|---|---|---|---|---|---|
| Dummy (lớp đa số) | 0.905 | 0.302 | 0.333 | 0.317 | 0.500 | 0.000 |
| LogisticRegression (baseline) | 0.923 | 0.597 | 0.424 | 0.458 | 0.907 | 0.000 |
| MultinomialNB (tuned) | 0.847 | 0.483 | 0.614 | 0.518 | 0.850 | 0.091 |
| **LogisticRegression (tuned)** | 0.919 | 0.575 | 0.621 | **0.593** | 0.884 | 0.154 |
| LinearSVC (tuned) | 0.929 | 0.671 | 0.573 | 0.597 | 0.877 | 0.207 |
| LogisticRegression (tuned + meta) | 0.919 | 0.554 | 0.600 | 0.572 | 0.880 | 0.103 |
| LinearSVC (tuned + meta) | 0.927 | 0.595 | 0.570 | 0.578 | 0.873 | 0.121 |

Báo cáo theo lớp của mô hình cuối:

| Lớp | Precision | Recall | F1 | Số mẫu |
|---|---|---|---|---|
| Tiêu cực | 0.578 | 0.771 | 0.661 | 48 |
| Trung tính | 0.176 | 0.136 | 0.154 | 22 |
| Tích cực | 0.971 | 0.955 | 0.963 | 667 |
| Macro | 0.575 | 0.621 | 0.593 | 737 |

ROC-AUC theo lớp: Tiêu cực 0,967 · Trung tính 0,745 · Tích cực 0,939. LinearSVC (tuned) cao hơn 0,004 F1 trên Test nhưng nằm trong sai số, và nhóm **không đổi mô hình the[...]

## 7. Trả lời hai câu hỏi của bài
**Câu 1 — Từ nào phân biệt ba lớp?**
- Tiêu cực: hỏng hóc/đòi quyền lợi và phủ định (*died, dead, failed, stopped, refund, return, lost*, cụm *not recommend*, *does not*, *card failed*).
- Tích cực: *great, works, works great, fast, good, best, love, price, space*, cụm *no problems*.
- Trung tính: từ yếu và phân tán (*but not, though, job, expectations*), không có từ đặc trưng rõ vì chỉ có khoảng 99 mẫu Train.

**Câu 2 — Xử lý mất cân bằng bắt thêm được bao nhiêu? (Test: 48 Tiêu cực, 22 Trung tính)**

| Cấu hình | Accuracy | F1 macro | Bắt Tiêu cực | Bắt Trung tính | Báo nhầm → Tiêu cực | Báo nhầm → Trung tính |
|---|---|---|---|---|---|---|
| 1. Baseline LogReg | 0.923 | 0.458 | 13 | 0 | 2 | 0 |
| 2. + class_weight | 0.904 | 0.577 | 40 | 3 | 37 | 19 |
| 3. Mô hình cuối (tuned) | 0.919 | 0.593 | 37 | 3 | 27 | 14 |

`class_weight='balanced'` giúp bắt Tiêu cực tăng từ 13 lên 37/48 (+24) với giá là thêm khoảng 25 cảnh báo sai (2 → 27). Lớp Trung tính chỉ bắt được **3/22**: xử [...] 

## 8. Phân tích lỗi
- Theo điểm sao (Test): 1★ đúng 77,1% (n=35), 2★ 76,9% (n=13), **3★ chỉ 13,6% (n=22)**, 4★ 90,1% (n=81), 5★ 96,2% (n=586).
- Đánh giá dài nhất (54–449 từ) đúng 80,4%, so với 94–97% ở các nhóm ngắn hơn: đánh giá dài thường vừa khen vừa chê.
- Kiểu nhầm nhiều nhất: Tích cực → Tiêu cực **20** (hệ quả của `class_weight`), Trung tính → Tích cực **12**, Tích cực → Trung tính 10.
- Ca "tự tin nhưng sai": khen trước chê sau, ẩn dụ ("Passed away... RIP"), phàn nàn về giá không dùng từ cảm xúc. Mô hình túi từ không hiểu ngữ cảnh, mỉa mai h[...]

## 9. Mở rộng
**4.5 — Tập ngoài (5.000 đánh giá, nhãn 0–4 → 1–5 sao; 40% Tiêu cực / 20% Trung tính / 40% Tích cực).** Không dùng để huấn luyện hay chọn mô hình.

| Mô hình | Accuracy | Precision | Recall | F1 macro | ROC-AUC | F1 Trung tính |
|---|---|---|---|---|---|---|
| LogisticRegression (baseline) | 0.408 | 0.452 | 0.340 | 0.205 | 0.720 | 0.000 |
| MultinomialNB (tuned) | 0.559 | 0.524 | 0.519 | 0.517 | 0.720 | 0.294 |
| **LogisticRegression (tuned)** | 0.496 | 0.523 | 0.432 | **0.389** | 0.729 | 0.164 |
| LinearSVC (tuned) | 0.471 | 0.538 | 0.399 | 0.325 | 0.721 | 0.075 |
| LogisticRegression (tuned + meta) | 0.451 | 0.504 | 0.391 | 0.321 | 0.698 | 0.141 |
| LinearSVC (tuned + meta) | 0.447 | 0.515 | 0.377 | 0.286 | 0.705 | 0.054 |

F1 macro của mô hình cuối giảm từ 0,593 (Test) xuống 0,389. Tỉ lệ bị đoán "Tích cực" theo nhãn gốc 0→4 là 63%, 70%, 81%, 91%, 96% (tăng đơn điệu, giả định [...] 

**4.6 — RoBERTa zero-shot (`cardiffnlp/twitter-roberta-base-sentiment-latest`).** Bản notebook đã lưu được chạy ở môi trường không có `torch`, nên **chưa có số liệu**.[...]

## 10. Kết luận, hạn chế, hướng phát triển
- Mô hình cuối (LogReg `C=3`, `balanced`): Accuracy 0,919, F1 macro 0,593, ROC-AUC 0,884; vượt Dummy (0,317) và baseline (0,458).
- Hạn chế: lớp Trung tính chỉ 142 mẫu (22 ở Test) nên số liệu rất nhiễu; nhãn suy ra từ điểm sao; mô hình túi từ không hiểu ngữ cảnh; không tổng quát h[...]
- Hướng phát triển: thêm đánh giá Trung tính, thử SMOTE/tăng cường dữ liệu, tinh chỉnh ngưỡng theo lớp, dùng embedding hoặc fine-tune Transformer, huấn luyện tr[...]
