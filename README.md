Giới thiệu
Bài toán 8 quân hậu là một bài toán nổi tiếng trong toán học và khoa học máy tính. Nó đòi hỏi người chơi phải đặt 8 quân hậu trên một bàn cờ tiêu chuẩn (8x8) mà không có quân hậu nào nằm trên cùng một hàng, cùng một cột hoặc cùng một đường chéo. Đây là một ví dụ tuyệt vời để minh họa cho các thuật toán tìm kiếm và quay lui (backtracking).

Dự án này cung cấp một giao diện trực quan để người chơi có thể tự mình thử sức giải bài toán hoặc xem máy tính tìm ra một trong 92 lời giải có thể có.

Luật chơi
Luật chơi rất đơn giản, dựa trên cách di chuyển của quân Hậu trong cờ vua:

Một hàng, một hậu: Mỗi hàng chỉ có thể có duy nhất một quân hậu.

Một cột, một hậu: Mỗi cột chỉ có thể có duy nhất một quân hậu.

Một đường chéo, một hậu: Mỗi đường chéo chỉ có thể có duy nhất một quân hậu.

Người chơi chiến thắng khi đặt thành công cả 8 quân hậu lên bàn cờ mà không vi phạm bất kỳ quy tắc nào ở trên.

Cách chơi
Chế độ người chơi:

Nhấp chuột vào một ô trống trên bàn cờ để đặt một quân hậu.

Nếu vị trí đặt vi phạm luật chơi (bị một quân hậu khác tấn công), một cảnh báo sẽ hiện ra.

Để di chuyển một quân hậu đã đặt, hãy nhấp vào quân hậu đó và sau đó nhấp vào vị trí mới.

Để xóa một quân hậu khỏi bàn cờ, hãy nhấp chuột phải vào quân hậu đó.

Trò chơi kết thúc khi bạn đặt thành công 8 quân hậu.

Chế độ máy tính giải:

Nhấn vào nút "Giải" (Solve) hoặc một nút tương tự.

Chương trình sẽ tự động tìm và hiển thị một lời giải cho bài toán.

Bạn có thể nhấn nút "Giải pháp khác" (Next Solution) để xem các lời giải khác nhau (nếu có).

Tính năng
Giao diện đồ họa trực quan: Bàn cờ được hiển thị rõ ràng, giúp người chơi dễ dàng tương tác.

Chế độ chơi linh hoạt: Cho phép người chơi tự giải đố hoặc xem máy tính trình diễn lời giải.

Kiểm tra nước đi hợp lệ: Tự động phát hiện và cảnh báo khi người chơi đặt quân hậu vào vị trí không hợp lệ.
Đóng góp
Nếu bạn muốn đóng góp cho dự án, vui lòng tạo một "pull request". Mọi sự đóng góp để cải thiện trò chơi đều được hoan nghênh.

Tác giả
Phạm Văn Hậu - 23110098 
Thuật toán giải đố: Tích hợp thuật toán quay lui (backtracking) để tìm ra lời giải một cách hiệu quả.

Hiển thị nhiều lời giải: Khả năng duyệt qua các lời giải khác nhau của bài toán.
