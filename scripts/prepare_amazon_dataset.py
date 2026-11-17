"""Kiểm tra dữ liệu của bài Text trước khi chạy notebook.

Cách dùng (chạy từ thư mục 02_Text):
    python scripts/prepare_amazon_dataset.py
    python scripts/prepare_amazon_dataset.py --data-dir data/text
Mã thoát: 0 nếu dữ liệu hợp lệ, 1 nếu thiếu file hoặc sai cột.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

EXPECTED_COLS = ['Unnamed: 0', 'reviewerName', 'overall', 'reviewText', 'reviewTime', 'day_diff', 'helpful_yes',
                 'helpful_no', 'total_vote', 'score_pos_neg_diff', 'score_average_rating', 'wilson_lower_bound']
CLASS_NAMES = {0: 'Tiêu cực (1-2 sao)', 1: 'Trung tính (3 sao)', 2: 'Tích cực (4-5 sao)'}


def check_main(path: Path) -> bool:
    if not path.exists():
        print(f'[LỖI] Không thấy {path}')
        return False
    df = pd.read_csv(path)
    ok = True
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        print(f'[LỖI] {path.name} thiếu cột: {missing}')
        ok = False
    print(f'{path.name}: {df.shape[0]:,} dòng × {df.shape[1]} cột (kỳ vọng 4,915 × 12)')
    if 'reviewText' in df.columns and 'overall' in df.columns:
        clean = df.dropna(subset=['reviewText']).drop_duplicates(subset='reviewText')
        labels = clean['overall'].map(lambda r: 0 if r <= 2 else (1 if r == 3 else 2))
        print(f'  Thiếu reviewText: {df["reviewText"].isna().sum()} | trùng nội dung: '
              f'{len(df.dropna(subset=["reviewText"])) - len(clean)} | còn lại: {len(clean):,}')
        for k, v in labels.value_counts().sort_index().items():
            print(f'  {CLASS_NAMES[k]}: {v:,} ({v / len(clean):.1%})')
    return ok


def check_external(path: Path) -> None:
    if not path.exists():
        print(f'[CẢNH BÁO] Không thấy {path.name}: notebook sẽ bỏ qua mục 4.5 (không gây lỗi).')
        return
    ext = pd.read_json(path, lines=True)
    miss = [c for c in ('text', 'label') if c not in ext.columns]
    if miss:
        print(f'[CẢNH BÁO] {path.name} thiếu cột {miss}')
        return
    print(f'{path.name}: {len(ext):,} dòng | nhãn gốc: {ext["label"].value_counts().sort_index().to_dict()}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--data-dir', default=str(Path(__file__).resolve().parents[1] / 'data' / 'text'))
    args = parser.parse_args()
    d = Path(args.data_dir)
    ok = check_main(d / 'amazon_reviews.csv')
    check_external(d / 'external_test.jsonl')
    print('=> Dữ liệu hợp lệ, có thể chạy notebook.' if ok else '=> Cần sửa dữ liệu trước khi chạy notebook.')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
