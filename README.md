# Đề tài: Giải bài toán người du lịch (traveller problem, travelling salesman problem) bằng Giải thuật quay lui (Backtracking)

---

# 📌 PHẦN CODE – PHÂN CÔNG & TRIỂN KHAI CHI TIẾT

## 👤 Thông – Kiến trúc dữ liệu & Nền tảng dùng chung

### 🎯 Mục tiêu

Xây dựng hệ thống nền tảng thống nhất để đảm bảo tất cả các thuật toán sử dụng chung một cấu trúc dữ liệu, tránh tình trạng mỗi người triển khai một kiểu gây khó khăn cho việc tích hợp và so sánh.

### 📌 Nhiệm vụ chi tiết

#### 1. Xây dựng bộ nạp dữ liệu (Data Loader)

* Hỗ trợ 2 hình thức:

  * Đọc dữ liệu từ file (`.txt`, `.json`)
  * Sinh dữ liệu ngẫu nhiên (tọa độ các thành phố)
* Nếu dùng tọa độ:

  * Tính ma trận khoảng cách bằng công thức Euclidean
* Đảm bảo output luôn là:

  ```python
  distance_matrix: np.ndarray (n x n)
  ```

#### 2. Viết các hàm tiện ích (Utility Functions)

* **Tính tổng chi phí đường đi**

  ```python
  calculate_total_distance(path, distance_matrix)
  ```

  * Input: danh sách thứ tự các thành phố
  * Output: tổng khoảng cách (bao gồm quay về điểm xuất phát)

* **Kiểm tra tính hợp lệ của đường đi**

  ```python
  is_valid_path(path, n)
  ```

  * Đảm bảo:

    * Không lặp thành phố
    * Đi qua đủ tất cả các thành phố

#### 3. Chuẩn hóa cấu trúc đầu ra

Thiết kế format chung để tất cả thuật toán trả về:

```python
result = {
    "path": [...],          # Danh sách thứ tự các thành phố
    "cost": float,          # Tổng chi phí
    "time": float           # Thời gian chạy (seconds)
}
```

👉 Mục đích: Giúp việc so sánh và báo cáo sau này đơn giản, không phải convert qua lại.

### 🛠 Công cụ sử dụng

* `numpy`
* `json` / file `.txt`

---

## 👤 Diệu – Giải thuật chính xác (Backtracking & Branch and Bound)

### 🎯 Mục tiêu

Tìm nghiệm tối ưu tuyệt đối (optimal solution) cho bài toán TSP với số lượng thành phố nhỏ.

### 📌 Nhiệm vụ chi tiết

#### 1. Triển khai Backtracking

* Sử dụng đệ quy để sinh tất cả hoán vị đường đi
* Duyệt toàn bộ không gian nghiệm

#### 2. Tối ưu hóa bằng Branch and Bound (Cắt tỉa)

Áp dụng điều kiện cắt:

```python
if current_cost >= best_cost:
    prune
```

* Nếu chi phí hiện tại đã lớn hơn nghiệm tốt nhất → bỏ nhánh
* Giảm đáng kể số lượng trạng thái cần duyệt

#### 3. Xác định giới hạn khả thi

* Thực nghiệm để tìm giá trị `n` tối đa
* Dự kiến:

  * Backtracking hiệu quả khi: `n < 15`
* Ghi nhận:

  * Thời gian chạy tăng theo cấp số nhân

---

## 👤 Nhi – Thuật toán Bat Algorithm (BA)

### 🎯 Mục tiêu

Giải bài toán TSP với số lượng thành phố lớn bằng thuật toán heuristic (xấp xỉ tối ưu).

### 📌 Nhiệm vụ chi tiết

#### 1. Mô hình hóa Bat Algorithm cho TSP

Vấn đề:

* BA gốc dùng không gian liên tục
* TSP là bài toán rời rạc

👉 Giải pháp:

* Biểu diễn mỗi “con dơi” bằng một hoán vị (permutation)
* Thay phép cộng vector bằng:

  * Swap operator
  * Swap sequence

#### 2. Thiết lập tham số

* Tần số (`f`)
* Cường độ âm (`A`)
* Tốc độ phát xung (`r`)

Cập nhật theo iteration:

* Giảm `A`
* Tăng `r`

#### 3. Cơ chế cập nhật vị trí

* Dơi di chuyển dựa trên:

  * Cá thể tốt nhất hiện tại (global best)
* Áp dụng:

  * Local search (tìm kiếm cục bộ)
  * Random walk khi cần

#### 4. Hàm đánh giá (Fitness Function)

* Sử dụng:

```python
calculate_total_distance(path)
```

---

## 👤 Phi – Kiểm thử, So sánh & Trực quan hóa

### 🎯 Mục tiêu

Đánh giá hiệu năng hai thuật toán và trình bày kết quả một cách trực quan, dễ hiểu.

### 📌 Nhiệm vụ chi tiết

#### 1. Đo lường hiệu năng

* Chạy trên cùng bộ dữ liệu:

  * 10 thành phố
  * 20 thành phố
  * 50 thành phố
  * 100 thành phố

* Ghi nhận:

  * Thời gian chạy
  * Chi phí đường đi

#### 2. So sánh kết quả

Lập bảng:

| Số thành phố | Backtracking Cost | BA Cost | Sai lệch | Thời gian BT | Thời gian BA |
| ------------ | ----------------- | ------- | -------- | ------------ | ------------ |

Phân tích:

* BA có đạt nghiệm tối ưu không?
* Nhanh hơn bao nhiêu lần?

#### 3. Trực quan hóa

* **Vẽ đường đi TSP**

  * Dùng `matplotlib`
  * Hiển thị:

    * Các thành phố
    * Đường nối theo thứ tự

* **Đồ thị hội tụ của BA**

  * Trục X: số iteration
  * Trục Y: cost tốt nhất
  * Quan sát tốc độ hội tụ

---
