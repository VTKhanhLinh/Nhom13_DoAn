
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "processed" / "clean_data.csv"
CLUSTER_FILE = BASE_DIR / "data" / "processed" / "clustered_data.csv"

st.set_page_config(
    page_title="Phân nhóm sinh viên",
    page_icon="🎓",
    layout="wide"
)

# Tải dữ liệu
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

st.title("🎓 PHÂN NHÓM SINH VIÊN")
st.subheader("Phân tích hành vi học tập bằng thuật toán phân cụm")

st.markdown("""
Ứng dụng hỗ trợ phân tích dữ liệu học tập và phân nhóm sinh viên
dựa trên những đặc điểm học tập tương đồng.

**Mục tiêu:**
- Khám phá đặc điểm và tình hình học tập của sinh viên.
- Phân nhóm sinh viên bằng thuật toán K-Means.
- Hỗ trợ nhận diện các nhóm có hành vi học tập khác nhau.
""")

st.divider()

# Đọc dữ liệu
df = None
error_message = None

if DATA_FILE.exists():
    try:
        df = load_data(str(DATA_FILE))
    except Exception as e:
        error_message = str(e)
else:
    error_message = "Không tìm thấy file clean_data.csv."

cluster_df = None
if CLUSTER_FILE.exists():
    try:
        cluster_df = load_data(str(CLUSTER_FILE))
    except Exception:
        pass

# Thống kê tổng quan
total_students = len(df) if df is not None else 0
total_features = df.shape[1] if df is not None else 0

if cluster_df is not None and "Cluster" in cluster_df.columns:
    total_clusters = cluster_df["Cluster"].nunique()
    cluster_label = str(total_clusters)
else:
    cluster_label = "Chưa phân cụm"

col1, col2, col3 = st.columns(3)
col1.metric("👨‍🎓 Tổng số sinh viên", f"{total_students:,}")
col2.metric("📊 Số thuộc tính", total_features)
col3.metric("🔍 Số cụm", cluster_label)

if error_message:
    st.warning(
        f"{error_message} "
        "Hãy kiểm tra đường dẫn và file dữ liệu trong thư mục data/processed."
    )

st.divider()

# Biểu đồ tổng quan
st.subheader("📈 Tổng quan dữ liệu học tập")

if df is not None and not df.empty:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    # Ưu tiên cột điểm tổng kết nếu tồn tại
    score_candidates = [
        col for col in numeric_columns
        if any(keyword in col.lower() for keyword in
               ["điểm tổng kết", "diem_tong_ket", "final_score",
                "final grade", "final_grade"])
    ]

    if score_candidates:
        score_col = score_candidates[0]
        chart_data = df[score_col].dropna()

        if not chart_data.empty:
            st.caption(f"Phân bố điểm theo thuộc tính: {score_col}")
            st.bar_chart(
                chart_data.value_counts(bins=10, sort=False)
                .sort_index()
            )
        else:
            st.info("Chưa có dữ liệu điểm hợp lệ để vẽ biểu đồ.")
    else:
        st.info(
            "Chưa tìm thấy cột điểm tổng kết phù hợp. "
            "M có thể xem dữ liệu ở trang Tổng quan."
        )
else:
    st.info("Chưa có dữ liệu để hiển thị biểu đồ.")

st.divider()

# Hướng dẫn sử dụng
st.subheader("🧭 Hướng dẫn sử dụng")

st.markdown("""
1. **Tổng quan:** xem dữ liệu, tìm kiếm sinh viên và lọc thuộc tính.
2. **Phân nhóm:** thực hiện hoặc xem kết quả phân cụm sinh viên.
3. **Gợi ý:** xem các nhận xét hoặc gợi ý dựa trên kết quả phân nhóm.

Chọn trang tương ứng ở **thanh điều hướng bên trái** để bắt đầu.
""")
