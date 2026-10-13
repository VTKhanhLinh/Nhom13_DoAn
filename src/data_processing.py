
"""Xử lý dữ liệu - Khánh Linh."""

from pathlib import Path
import pandas as pd

# Đường dẫn tương đối với thư mục dự án
ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "student_data.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "clean_data.csv"

# Các cột không sử dụng trong bản dữ liệu làm việc
DROP_COLUMNS = ["Email", "Grade"]

# Đổi tên các thuộc tính sang tiếng Việt
COLUMN_NAMES_VI = {
    "Student_ID": "Mã sinh viên",
    "First_Name": "Tên",
    "Last_Name": "Họ",
    "Gender": "Giới tính",
    "Age": "Tuổi",
    "Department": "Ngành học",
    "Attendance (%)": "Tỷ lệ chuyên cần (%)",
    "Midterm_Score": "Điểm giữa kỳ",
    "Final_Score": "Điểm cuối kỳ",
    "Assignments_Avg": "Điểm bài tập trung bình",
    "Quizzes_Avg": "Điểm kiểm tra ngắn trung bình",
    "Participation_Score": "Điểm tham gia học tập",
    "Projects_Score": "Điểm dự án",
    "Total_Score": "Điểm tổng kết",
    "test_preparation_course": "Tham gia khóa ôn tập",
    "math_score": "Điểm Toán",
    "reading_score": "Điểm Đọc hiểu",
    "writing_score": "Điểm Viết",
    "science_score": "Điểm Khoa học"
}


def clean_data():
    # 1. Đọc dữ liệu gốc
    df = pd.read_csv(INPUT_FILE)

    print("=== DU LIEU BAN DAU ===")
    print("So dong:", len(df))
    print("So cot:", len(df.columns))
    print("Gia tri thieu:", df.isna().sum().sum())
    print("Dong trung:", df.duplicated().sum())

    # 2. Kiểm tra các cột cần thiết
    required_columns = [
        "Student_ID",
        "First_Name",
        "Last_Name",
        "math_score",
        "Email",
        "Grade",
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Thieu cot bat buoc: {missing_columns}"
        )

    # 3. Làm sạch math_score
    original_math = df["math_score"].copy()

    cleaned_math = (
        df["math_score"]
        .astype("string")
        .str.replace(r"\t", "", regex=False)
        .str.replace("\t", "", regex=False)
        .str.strip()
    )

    df["math_score"] = pd.to_numeric(
        cleaned_math,
        errors="coerce"
    )

    invalid_math = df["math_score"].isna().sum()

    if invalid_math > 0:
        raise ValueError(
            f"Con {invalid_math} gia tri math_score khong hop le."
        )

    print(
        "So gia tri math_score duoc thay doi:",
        (original_math.astype("string") != cleaned_math).sum()
    )

    # 4. Loại hai cột không dùng
    df = df.drop(columns=DROP_COLUMNS)

    # 5. Kiểm tra ID sinh viên
    if df["Student_ID"].isna().any():
        raise ValueError("Student_ID co gia tri thieu.")

    if df["Student_ID"].duplicated().any():
        raise ValueError("Student_ID bi trung.")

    # 6. Kiểm tra dữ liệu sau xử lý
    print("\n=== DU LIEU SAU XU LY ===")
    print("So dong:", len(df))
    print("So cot:", len(df.columns))
    print("Gia tri thieu:", df.isna().sum().sum())
    print("Dong trung:", df.duplicated().sum())
    print("Kieu math_score:", df["math_score"].dtype)

    if df.isna().sum().sum() > 0:
        raise ValueError(
            "Du lieu sau xu ly van co gia tri thieu."
        )

    if df.shape[1] != 19:
        raise ValueError(
            "So cot sau xu ly khong bang 19."
        )

    # 7. Đổi tên các thuộc tính sang tiếng Việt
    df = df.rename(columns=COLUMN_NAMES_VI)

    print("\n=== TEN COT SAU KHI DOI ===")
    for col in df.columns:
        print("-", col)

    # 8. Lưu dữ liệu sạch
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDa luu:", OUTPUT_FILE)
    print("CLEAN DATA OK!")


if __name__ == "__main__":
    clean_data()
