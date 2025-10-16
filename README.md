👑 Trực quan hóa Giải thuật Bài toán 8 Quân Hậu
Dự án này là một ứng dụng desktop được xây dựng bằng Python và Tkinter để trực quan hóa quá trình giải quyết Bài toán 8 Quân Hậu bằng nhiều thuật toán Trí tuệ Nhân tạo khác nhau. Mục tiêu chính là cung cấp một công cụ học tập sinh động, giúp người dùng hiểu rõ hơn về cách hoạt động, ưu và nhược điểm của từng thuật toán.

✨ Tính năng chính
Giao diện đồ họa trực quan: Sử dụng Tkinter để tạo ra một giao diện thân thiện, dễ sử dụng.

Minh họa từng bước: Hiển thị từng bước đi của thuật toán, từ trạng thái ban đầu đến khi tìm ra lời giải.

Hỗ trợ đa dạng thuật toán: Cài đặt hơn 15 thuật toán kinh điển thuộc nhiều trường phái khác nhau (tìm kiếm mù, tìm kiếm có thông tin, tìm kiếm cục bộ, CSP,...).

Điều khiển linh hoạt: Cho phép người dùng xem từng bước (Bước tiếp theo), bỏ qua đến lời giải cuối cùng (Bỏ qua), hoặc tự động chạy (auto-run).

Tùy chỉnh tốc độ: Dễ dàng thay đổi tốc độ của chế độ auto-run trong file cấu hình.

🚀 Các thuật toán được cài đặt
Dự án bao gồm một bộ sưu tập phong phú các thuật toán, được phân loại như sau:

1. Tìm kiếm mù (Uninformed Search)
BFS (Breadth-First Search): Tìm kiếm theo chiều rộng, đảm bảo tìm ra lời giải ở độ sâu nông nhất.

DFS (Depth-First Search): Tìm kiếm theo chiều sâu, đi sâu vào một nhánh cho đến khi hết đường.

UCS (Uniform Cost Search): Tìm kiếm chi phí thấp nhất, mở rộng nút có chi phí đường đi nhỏ nhất từ gốc.

DLS (Depth-Limited Search): Tương tự DFS nhưng có giới hạn về độ sâu.

IDS (Iterative Deepening Search): Kết hợp ưu điểm của BFS và DFS.

2. Tìm kiếm có thông tin (Informed Search)
Greedy Search: Tìm kiếm tham lam, luôn chọn hướng đi có vẻ tốt nhất tại thời điểm hiện tại dựa trên hàm heuristic.

A* Search (A-Star): Kết hợp chi phí thực tế (g) và chi phí ước tính (h) để tìm đường đi tối ưu.

3. Tìm kiếm cục bộ (Local Search) & Thuật toán Metaheuristic
Hill Climbing: Leo đồi, luôn di chuyển đến trạng thái lân cận tốt hơn.

Simulated Annealing: Mô phỏng luyện kim, cho phép di chuyển đến trạng thái xấu hơn với một xác suất nhất định để tránh bị kẹt ở tối ưu cục bộ.

Beam Search: Giữ lại một số lượng (beam_width) trạng thái tốt nhất ở mỗi bước để khám phá tiếp.

Genetic Algorithm: Thuật toán di truyền, mô phỏng quá trình tiến hóa tự nhiên (lai ghép, đột biến) để tìm lời giải.

4. Các thuật toán nâng cao
And-Or Search: Phù hợp cho các bài toán có thể được phân rã thành các bài toán con.

Belief Space Search: Tìm kiếm trong không gian "niềm tin", sử dụng mô hình xác suất để hướng dẫn quá trình tìm kiếm, tương tự như các thuật toán tối ưu hóa phân bố ước lượng (EDA).

Partial Search: Một phương pháp tiếp cận tùy chỉnh, giải quyết bài toán bằng cách đặt một vài quân hậu một lúc thay vì từng quân một.

5. Giải bài toán ràng buộc (Constraint Satisfaction Problems - CSP)
Backtracking: Quay lui, thuật toán nền tảng cho các bài toán CSP, thử và sai một cách có hệ thống.

Forward Checking: Cải tiến của Backtracking, sau khi gán một giá trị cho biến, nó sẽ kiểm tra và loại bỏ các giá trị không tương thích trong miền của các biến chưa được gán.

AC-3 (Arc Consistency Algorithm #3): Một thuật toán dùng để tiền xử lý, đảm bảo tính nhất quán cung giữa các biến để loại bỏ các giá trị không thể có trước khi bắt đầu tìm kiếm.

🛠️ Công nghệ sử dụng
Ngôn ngữ: Python 3

Thư viện giao diện: Tkinter

Xử lý hình ảnh: Pillow (PIL)

Thao tác ma trận: NumPy

⚙️ Cài đặt và Chạy dự án
Yêu cầu
Python 3.6+

Pip

Các bước cài đặt
Clone repository về máy:

Bash

git clone <URL_CUA_REPOSITORY>
cd <TEN_THU_MUC_DU_AN>
(Khuyến khích) Tạo và kích hoạt môi trường ảo:

Bash

python -m venv venv
# Trên Windows
.\venv\Scripts\activate
# Trên macOS/Linux
source venv/bin/activate
Cài đặt các thư viện cần thiết:

Bash

pip install numpy Pillow
Chạy ứng dụng: Đảm bảo file ảnh queen_white.png nằm cùng cấp với các file script.

Bash

python main.py
📖 Hướng dẫn sử dụng
Chạy chương trình: Mở ứng dụng bằng lệnh python main.py.

Chọn thuật toán: Ở khung bên phải, chọn một thuật toán từ danh sách.

Bắt đầu giải: Nhấn nút "Giải bài toán". Thuật toán sẽ bắt đầu chạy và hiển thị trạng thái ban đầu trên bàn cờ bên phải.

Theo dõi quá trình:

Đối với các thuật toán như Hill Climbing, Genetic Algorithm,...:

Nhấn "Bước tiếp theo" để xem từng bước lặp của thuật toán.

Nhấn "Bỏ qua" để nhảy đến trạng thái cuối cùng (lời giải nếu tìm thấy).

Chế độ auto-run sẽ tự động chạy qua tất cả các bước.

Đối với các thuật toán như BFS, DFS,... (tìm nhiều lời giải):

Chương trình sẽ tự động chạy các bước để tìm ra lời giải đầu tiên.

Nhấn "Phương án kế tiếp" để xem quá trình tìm ra lời giải tiếp theo.

Nhấn "Bỏ qua" để hiển thị ngay lập tức lời giải hiện tại mà không cần xem các bước trung gian.

📂 Cấu trúc dự án
.
├── main.py             # File chính, xử lý giao diện và luồng sự kiện
├── algorithms.py       # Chứa logic cài đặt tất cả các thuật toán
├── board.py            # Chứa các hàm tiện ích liên quan đến bàn cờ (hiển thị, kiểm tra)
├── queen_white.png     # Ảnh quân hậu
└── README.md           # File này
