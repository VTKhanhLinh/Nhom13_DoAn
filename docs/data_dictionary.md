
# TỪ ĐIỂN DỮ LIỆU SINH VIÊN

## 1. Thông tin chung

Đề tài: Ứng dụng K-Means trong phân nhóm sinh viên
dựa trên hành vi học tập nhằm hỗ trợ cá nhân hóa
phương pháp học tập.

- Nguồn: Kaggle
- Dữ liệu gốc: 10.000 dòng, 21 cột
- Dữ liệu sau xử lý: 10.000 dòng, 19 cột
- File gốc: data/raw/student_data.csv
- File sạch: data/processed/clean_data.csv

## 2. Danh sách thuộc tính

| Thuộc tính | Ý nghĩa | Vai trò |
|---|---|---|
| Student_ID | Mã sinh viên | Định danh |
| First_Name | Tên sinh viên | Hiển thị |
| Last_Name | Họ sinh viên | Hiển thị |
| Gender | Giới tính | Thống kê |
| Age | Tuổi | Thống kê |
| Department | Ngành học | Thống kê |
| Attendance (%) | Tỷ lệ chuyên cần | Đặc trưng K-Means |
| Midterm_Score | Điểm giữa kỳ | Phân tích kết quả |
| Final_Score | Điểm cuối kỳ | Phân tích kết quả |
| Assignments_Avg | Điểm bài tập trung bình | Đặc trưng K-Means |
| Quizzes_Avg | Điểm kiểm tra ngắn | Đặc trưng K-Means |
| Participation_Score | Mức độ tham gia học tập | Đặc trưng K-Means |
| Projects_Score | Điểm dự án | Đặc trưng K-Means |
| Total_Score | Điểm tổng kết được cung cấp | Phân tích kết quả |
| test_preparation_course | Tham gia khóa chuẩn bị kiểm tra | Phân tích bổ sung |
| math_score | Điểm Toán | Phân tích kết quả |
| reading_score | Điểm đọc hiểu | Phân tích kết quả |
| writing_score | Điểm viết | Phân tích kết quả |
| science_score | Điểm Khoa học | Phân tích kết quả |

## 3. Quy trình tiền xử lý

1. Đọc dữ liệu từ student_data.csv.
2. Kiểm tra dữ liệu thiếu và trùng lặp.
3. Làm sạch ký tự bất thường trong math_score.
4. Chuyển math_score sang kiểu số.
5. Loại Email và Grade khỏi bản dữ liệu làm việc.
6. Xuất clean_data.csv.

## 4. Đặc trưng phân cụm đề xuất

- Attendance (%)
- Assignments_Avg
- Quizzes_Avg
- Participation_Score
- Projects_Score

Các đặc trưng được chuẩn hóa trong pipeline
của mô hình trước khi chạy K-Means.

Không đưa mã sinh viên, họ tên hoặc email
vào thuật toán phân cụm.

## 5. Lưu ý khi phân tích

- Grade trong dữ liệu gốc không nhất quán
  với Total_Score nên đã được loại khỏi
  bản dữ liệu làm việc.
- Total_Score được giữ để phân tích,
  chưa xác minh công thức tính.
- Các đặc trưng liên quan đến điểm bài tập,
  kiểm tra và dự án là chỉ báo gián tiếp
  về hành vi học tập, không phản ánh đầy đủ
  thói quen tự học của sinh viên.
- Số cụm và ý nghĩa từng cụm chỉ được xác định
  sau khi huấn luyện và phân tích kết quả.
