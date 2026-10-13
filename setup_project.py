
from pathlib import Path

ROOT = Path(__file__).resolve().parent

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "src",
    "models",
    "app/pages",
    "report",
    "slides",
]

for folder in folders:
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    (path / ".gitkeep").touch(exist_ok=True)

files = {
    ".gitignore": """.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.vscode/
""",

    "requirements.txt": """pandas
numpy
matplotlib
seaborn
scikit-learn
streamlit
joblib
jupyter
ipykernel
openpyxl
""",

    "README.md": """# NHÓM 13 - ĐỒ ÁN KHAI THÁC DỮ LIỆU

## Tên đề tài
Ứng dụng phân nhóm sinh viên dựa trên hành vi học tập
nhằm hỗ trợ cá nhân hóa phương pháp học tập.

## Thuật toán
K-Means Clustering

## Công nghệ
- Python 3.12.9
- VS Code
- GitHub
- Pandas, NumPy
- Scikit-learn
- Streamlit

## Phân công
- A: Trưởng nhóm, dữ liệu, EDA và báo cáo.
- B: Xây dựng và đánh giá mô hình K-Means.
- C: Xây dựng ứng dụng Streamlit.

## Cấu trúc dự án
- data/raw: Dữ liệu gốc
- data/processed: Dữ liệu sau xử lý
- notebooks: Phân tích và thử nghiệm
- src: Mã nguồn Python
- models: Mô hình đã huấn luyện
- app: Ứng dụng Streamlit
- report: Báo cáo Word
- slides: PowerPoint

## Trạng thái
Đang lựa chọn bộ dữ liệu.
""",

    "src/__init__.py": "",

    "src/data_processing.py": '"""Xử lý dữ liệu - thành viên A."""\n',

    "src/model.py": '"""Mô hình K-Means - thành viên B."""\n',

    "src/recommendation.py": '"""Gợi ý học tập - thành viên C, phối hợp A và B."""\n',

    "app/main.py": '''import streamlit as st

st.set_page_config(
    page_title="Phân nhóm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("Ứng dụng phân nhóm sinh viên")
st.write("Phân nhóm hành vi học tập bằng K-Means.")
st.info("Dự án đang trong giai đoạn phát triển.")
''',

    "app/pages/1_Tong_quan.py": '''import streamlit as st

st.title("Tổng quan")
st.info("Chưa có dữ liệu chính thức.")
''',

    "app/pages/2_Phan_nhom.py": '''import streamlit as st

st.title("Phân nhóm sinh viên")
st.info("Chưa có mô hình K-Means.")
''',

    "app/pages/3_Goi_y.py": '''import streamlit as st

st.title("Gợi ý học tập")
st.info("Chức năng đang được phát triển.")
''',
}

for filename, content in files.items():
    path = ROOT / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"Đã tồn tại, giữ nguyên: {filename}")
        continue

    path.write_text(content, encoding="utf-8")
    print(f"Đã tạo: {filename}")

print("\nSETUP PROJECT OK!")
