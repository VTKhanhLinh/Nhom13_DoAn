
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "data" / "processed" / "clean_data.csv"
CLUSTER_FILE = BASE_DIR / "data" / "processed" / "clustered_data.csv"

st.set_page_config(
    page_title="Phân nhóm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 PHÂN NHÓM SINH VIÊN")
st.subheader("Phân nhóm theo hành vi học tập bằng K-Means")

st.write("""
Chọn các thuộc tính học tập và số cụm K để phân nhóm sinh viên.
Hệ thống sẽ chuẩn hóa dữ liệu, thực hiện K-Means và hiển thị kết quả.
""")

# 1. Đọc dữ liệu
if not DATA_FILE.exists():
    st.error(f"Không tìm thấy dữ liệu: {DATA_FILE}")
    st.stop()

try:
    df = pd.read_csv(DATA_FILE)
except Exception as e:
    st.error(f"Không thể đọc dữ liệu: {e}")
    st.stop()

if df.empty:
    st.warning("Dataset hiện không có dữ liệu.")
    st.stop()

st.divider()
st.subheader("1. Chọn thuộc tính phân cụm")

# Chỉ lấy các cột số để phân cụm
numeric_columns = df.select_dtypes(include="number").columns.tolist()

# Loại cột ID nếu có
feature_options = [
    col for col in numeric_columns
    if not any(key in col.lower() for key in
               ["student_id", "studentid", "mssv", "ma_sinh_vien", "id"])
]

if len(feature_options) < 2:
    st.error("Cần ít nhất 2 thuộc tính dạng số để thực hiện phân cụm.")
    st.stop()

# Ưu tiên các thuộc tính hành vi học tập nếu tồn tại
preferred_features = [
    "Attendance (%)",
    "Assignments_Avg",
    "Quizzes_Avg",
    "Participation_Score",
    "Projects_Score",
    "Tỷ lệ chuyên cần (%)",
    "Điểm bài tập trung bình",
    "Điểm kiểm tra ngắn trung bình",
    "Điểm tham gia học tập",
    "Điểm dự án"
]

default_features = [
    col for col in preferred_features if col in feature_options
]

if len(default_features) < 2:
    default_features = feature_options[:min(5, len(feature_options))]

selected_features = st.multiselect(
    "Chọn các thuộc tính dùng để phân cụm",
    options=feature_options,
    default=default_features,
    help="Nên chọn các thuộc tính phản ánh hành vi và kết quả học tập."
)

st.caption(f"Đã chọn {len(selected_features)} thuộc tính.")

st.divider()
st.subheader("2. Cấu hình K-Means")

k = st.slider(
    "Số cụm K",
    min_value=2,
    max_value=10,
    value=3,
    step=1
)

st.caption(
    "K là số nhóm sinh viên mà thuật toán sẽ tạo ra. "
    "M có thể thử nhiều giá trị K để so sánh."
)

run_clustering = st.button(
    "🚀 Thực hiện phân cụm",
    type="primary",
    use_container_width=True
)

# 2. Thực hiện phân cụm khi người dùng bấm nút
if run_clustering:
    if len(selected_features) < 2:
        st.error("M hãy chọn ít nhất 2 thuộc tính.")
        st.stop()

    # Chuyển dữ liệu về dạng số
    X = df[selected_features].apply(
        pd.to_numeric, errors="coerce"
    )

    # Loại các hàng không có bất kỳ giá trị số nào
    valid_rows = X.notna().any(axis=1)
    X_valid = X.loc[valid_rows].copy()

    if len(X_valid) <= k:
        st.error(
            f"Cần nhiều hơn {k} bản ghi có dữ liệu hợp lệ để phân cụm."
        )
        st.stop()

    # Điền giá trị thiếu bằng trung vị
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X_valid)

    # Loại cột không có biến thiên sau xử lý
    varying_mask = X_imputed.std(axis=0) > 0

    if varying_mask.sum() < 2:
        st.error(
            "Cần ít nhất 2 thuộc tính có giá trị thay đổi "
            "giữa các sinh viên."
        )
        st.stop()

    X_imputed = X_imputed[:, varying_mask]
    used_features = [
        col for col, keep in zip(selected_features, varying_mask)
        if keep
    ]

    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Huấn luyện K-Means theo lựa chọn của người dùng
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    # Tạo kết quả, giữ các hàng không hợp lệ với Cluster rỗng
    result = df.copy()
    result["Cluster"] = pd.Series(
        pd.NA, index=result.index, dtype="Int64"
    )
    result.loc[X_valid.index, "Cluster"] = labels

    # Lưu kết quả để trang Tổng quan đọc
    try:
        CLUSTER_FILE.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(
            CLUSTER_FILE,
            index=False,
            encoding="utf-8-sig"
        )
    except Exception as e:
        st.error(f"Không thể lưu kết quả: {e}")
        st.stop()

    st.session_state["cluster_result"] = result
    st.session_state["cluster_features"] = used_features
    st.session_state["cluster_k"] = k
    st.session_state["cluster_silhouette"] = None

    # Silhouette chỉ tính khi các điều kiện hợp lệ
    if 1 < len(set(labels)) < len(labels):
        try:
            score = silhouette_score(X_scaled, labels)
            st.session_state["cluster_silhouette"] = score
        except Exception:
            pass

# 3. Hiển thị kết quả gần nhất trong phiên
result = st.session_state.get("cluster_result")

if result is not None:
    st.divider()
    st.subheader("3. Kết quả phân cụm")

    labels_valid = result["Cluster"].dropna().astype(int)
    cluster_counts = labels_valid.value_counts().sort_index()

    col1, col2, col3 = st.columns(3)
    col1.metric("Sinh viên được phân cụm", f"{len(labels_valid):,}")
    col2.metric("Số cụm thực tế", labels_valid.nunique())

    silhouette = st.session_state.get("cluster_silhouette")
    col3.metric(
        "Silhouette Score",
        f"{silhouette:.3f}" if silhouette is not None else "Chưa tính"
    )

    st.caption(
        "Silhouette Score càng gần 1 thường cho thấy các cụm "
        "tách biệt tốt hơn; kết quả còn phụ thuộc đặc điểm dữ liệu."
    )

    # Biểu đồ số lượng sinh viên trong từng cụm
    st.subheader("📊 Số lượng sinh viên theo cụm")

    chart_df = cluster_counts.rename_axis("Cụm").reset_index(
        name="Số sinh viên"
    )
    chart_df["Cụm"] = chart_df["Cụm"].astype(str)

    st.bar_chart(
        chart_df,
        x="Cụm",
        y="Số sinh viên",
        x_label="Cụm K-Means",
        y_label="Số sinh viên"
    )
    st.subheader("📊 Đặc điểm trung bình của từng cụm")

    profile = result.groupby("Cluster")[selected_features].mean().round(2)

    st.dataframe(profile, use_container_width=True)
        
# Phân tích ngành học theo từng cụm
    st.divider()
    st.subheader("🎓 Cơ cấu ngành học trong từng cụm")

# Tìm cột ngành học, không phân biệt chữ hoa/thường
    major_col = next(
        (col for col in result.columns if col.strip().lower() in
        ["ngành học", "nganh hoc", "major", "department"]),
        None
    )

    if major_col is None:
        st.warning(
        "Không tìm thấy cột ngành học trong dữ liệu. "
        "Hãy kiểm tra tên cột trong clean_data.csv."
    )
    else:
        major_data = result.dropna(subset=["Cluster", major_col]).copy()
        major_data["Cluster"] = major_data["Cluster"].astype(int)

    # Đếm số sinh viên theo cụm và ngành học
        major_counts = pd.crosstab(
           major_data["Cluster"],
           major_data[major_col]
    )

    # Bảng số lượng sinh viên
    st.markdown("**Số lượng sinh viên theo ngành và cụm**")
    st.dataframe(major_counts, use_container_width=True)

    # Biểu đồ cơ cấu ngành học
    st.markdown("**Biểu đồ phân bố ngành học trong từng cụm**")
    st.bar_chart(major_counts)

    # Tỷ lệ ngành học bên trong từng cụm
    st.markdown("**Tỷ lệ ngành học trong mỗi cụm (%)**")
    major_percent = (
        major_counts.div(major_counts.sum(axis=1), axis=0) * 100
    ).round(2)

    st.dataframe(major_percent, use_container_width=True)
    
    # Gợi ý học tập theo đặc điểm từng cụm
    st.divider()
    st.subheader("💡 Gợi ý học tập theo từng cụm")

    # Các thuộc tính dùng để đánh giá và đưa ra gợi ý
    feature_advice = {
        "Tỷ lệ chuyên cần (%)":
            "Nên duy trì việc đi học đầy đủ và đúng giờ.",
        "Điểm bài tập trung bình":
            "Nên luyện tập thêm bài tập và ôn lại kiến thức chưa vững.",
        "Điểm kiểm tra ngắn trung bình":
            "Nên ôn tập thường xuyên và luyện các bài kiểm tra ngắn.",
        "Điểm tham gia học tập":
            "Nên tích cực phát biểu, thảo luận và tham gia hoạt động trên lớp.",
        "Điểm dự án":
            "Nên cải thiện kỹ năng thực hành, lập kế hoạch và hoàn thành dự án."
    }

    # Dùng chính các thuộc tính đã chọn để phân cụm
    advice_features = [
        col for col in selected_features
        if col in result.columns
        and pd.api.types.is_numeric_dtype(result[col])
    ]

    if advice_features:
        advice_profile = (
            result.dropna(subset=["Cluster"])
            .groupby("Cluster")[advice_features]
            .mean()
        )

        # Trung bình toàn bộ sinh viên để làm mốc so sánh
        overall_mean = result[advice_features].mean()

        # Ngưỡng này dùng để tránh nhận xét chênh lệch quá nhỏ
        threshold = 0.05

        for cluster_id, row in advice_profile.iterrows():
            st.markdown(f"### 🎓 Cụm {int(cluster_id)}")

            cluster_size = int(
                (result["Cluster"] == cluster_id).sum()
            )
            st.write(f"Số sinh viên trong cụm: **{cluster_size:,}**")

            suggestions = []

            for feature in advice_features:
                mean_value = row[feature]
                overall_value = overall_mean[feature]

                if pd.isna(mean_value) or pd.isna(overall_value):
                    continue

                # So sánh tương đối với mức trung bình chung
                if overall_value != 0:
                    relative_diff = (
                        mean_value - overall_value
                    ) / abs(overall_value)
                else:
                    relative_diff = 0

                advice = feature_advice.get(feature)

                if relative_diff < -threshold and advice:
                    suggestions.append(
                        f"**{feature}** thấp hơn mức trung bình chung "
                        f"({mean_value:.2f} so với {overall_value:.2f}). "
                        f"{advice}"
                    )

            if suggestions:
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
            else:
                st.info(
                    "Các thuộc tính đã chọn không thấp hơn đáng kể "
                    "so với mức trung bình chung. Hãy tiếp tục duy trì "
                    "và phát huy những điểm mạnh hiện có."
                )

            st.markdown("**Giá trị trung bình của cụm:**")
            st.dataframe(
                row.to_frame(name="Điểm trung bình").round(2),
                use_container_width=True
            )
    else:
        st.info(
            "Không có thuộc tính số phù hợp để tạo gợi ý học tập."
        )


    # Bảng kết quả
    st.subheader("📋 Danh sách sinh viên")

    available_clusters = sorted(labels_valid.unique().tolist())
    selected_clusters = st.multiselect(
        "Lọc theo cụm",
        options=available_clusters,
        default=available_clusters
    )

    filtered_result = result[
        result["Cluster"].isin(selected_clusters)
    ]

    st.dataframe(filtered_result, use_container_width=True)

    st.caption(
        f"Đang hiển thị {len(filtered_result):,} / "
        f"{len(labels_valid):,} sinh viên đã phân cụm."
    )

    # Tải kết quả CSV
    csv_data = result.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        "⬇️ Tải kết quả phân cụm CSV",
        data=csv_data,
        file_name="clustered_data.csv",
        mime="text/csv"
    )
else:
    st.info(
        "Chưa có kết quả phân cụm trong phiên này. "
        "Hãy chọn thuộc tính, chọn K rồi nhấn "
        "**Thực hiện phân cụm**."
    )
