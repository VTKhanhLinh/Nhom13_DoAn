
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import joblib

st.title("Tổng quan")
st.info("Chưa có dữ liệu chính thức.")

# Cau hinh duong dan du lieu
BASE_DIR = Path(__file__).resolve().parents[2]
CLUSTER_FILE = BASE_DIR / "data" / "processed" / "student_clusters.csv"
DATA_FILE = BASE_DIR / "data" / "processed" / "clean_data.csv"
MODEL_FILE = BASE_DIR / "models" / "kmeans_model.pkl"
SCALER_FILE = BASE_DIR / "models" / "scaler.pkl"

st.title("Tổng quan dữ liệu sinh viên")
st.write(
    "Hệ thống phân nhóm sinh viên dựa trên hành vi học tập, "
    "giúp khám phá các nhóm có đặc điểm học tập tương đồng."
)

st.divider()

# Kiem tra du lieu
if not DATA_FILE.exists():
    st.warning(
        f"Chưa tìm thấy dữ liệu tại: {DATA_FILE}\n\n"
        "Hãy đặt file dữ liệu sinh viên vào thư mục data/raw "
        "và cập nhật tên file nếu cần."
    )
    st.stop()

df = pd.read_csv(DATA_FILE)

# Doc ket qua phan cum neu da co
if CLUSTER_FILE.exists():
    cluster_df = pd.read_csv(CLUSTER_FILE)
else:
    cluster_df = None

# Cac the thong ke
total_students = len(df)
total_features = df.shape[1]

if cluster_df is not None and "Cluster" in cluster_df.columns:
    total_clusters = cluster_df["Cluster"].nunique()
    cluster_label = str(total_clusters)
else:
    cluster_label = "Chưa phân cụm"

col1, col2, col3 = st.columns(3)

col1.metric("Tổng số sinh viên", f"{total_students:,}")
col2.metric("Số thuộc tính", total_features)
col3.metric("Số cụm", cluster_label)

st.divider()

# Tim kiem

# Tim kiem sinh vien
st.subheader("Danh sách sinh viên")

# Ho tro ca ten cot tieng Viet va tieng Anh
search_candidates = [
    "Tên", "Họ", "Mã sinh viên",
    "name", "student_name", "student_id", "studentid",
    "ma_sinh_vien", "ten_sinh_vien"
]

search_columns = [
    col for col in df.columns
    if col.strip().lower() in [x.lower() for x in search_candidates]
]

df_view = df.copy()

if search_columns:
    keyword = st.text_input("Tìm tên hoặc mã sinh viên")

    if keyword.strip():
        mask = df_view[search_columns].astype(str).apply(
            lambda col: col.str.contains(
                keyword.strip(), case=False, na=False
            )
        ).any(axis=1)

        df_view = df_view[mask]
else:
    st.caption("Không tìm thấy cột tên hoặc mã sinh viên trong dữ liệu.")
df_view = df.copy()

# Bo loc theo cot
filter_columns = st.multiselect(
    "Chọn thuộc tính để lọc",
    options=df.columns.tolist(),
    key="filter_columns"
)

for column in filter_columns:
    values = df_view[column].dropna().unique().tolist()
    if 0 < len(values) <= 30:
        selected = st.multiselect(
            f"Lọc {column}",
            options=values,
            default=values,
            key=f"filter_{column}"
        )
        df_view = df_view[df_view[column].isin(selected)]

st.dataframe(df_view, use_container_width=True)

st.caption(
    f"Đang hiển thị {len(df_view):,} / {len(df):,} bản ghi."
)

# Bieu do phan bo

# Biểu đồ phân bố sinh viên theo cụm K-Means
st.subheader("📊 Phân bố sinh viên theo cụm")

if cluster_df is not None and "Cluster" in cluster_df.columns:
    cluster_counts = (
        cluster_df["Cluster"]
        .value_counts()
        .sort_index()
    )

    chart_df = cluster_counts.rename_axis("Cụm").reset_index(name="Số sinh viên")
    chart_df["Cụm"] = chart_df["Cụm"].astype(str)

    st.bar_chart(
        chart_df,
        x="Cụm",
        y="Số sinh viên",
        x_label="Cụm K-Means",
        y_label="Số sinh viên"
    )

    st.caption(
        f"Tổng số sinh viên đã phân cụm: {cluster_counts.sum():,}"
    )
else:
    st.info(
        "Chưa có kết quả phân cụm. "
        "Hãy thực hiện phân nhóm ở trang Phân nhóm trước."
    )

