# Phần mềm Tách nền Ảnh (Background Removal)

Một ứng dụng máy tính đơn giản được viết bằng Python và Tkinter, cho phép người dùng dễ dàng xóa nền khỏi hình ảnh chỉ với vài cú nhấp chuột.

## Tính năng

- Giao diện đồ họa trực quan, dễ sử dụng.
- Chọn ảnh từ máy tính (hỗ trợ các định dạng phổ biến như PNG, JPG, WEBP).
- Tự động tách nền bằng mô hình AI mạnh mẽ từ thư viện `rembg`.
- Hiển thị song song ảnh gốc và ảnh kết quả.
- Lưu ảnh đã tách nền với định dạng PNG (để giữ nền trong suốt).

## Ảnh chụp màn hình

*(Bạn có thể đặt ảnh chụp màn hình của ứng dụng đang chạy ở đây)*

## Cài đặt

Để chạy được ứng dụng, bạn cần cài đặt Python và các thư viện cần thiết.

1.  **Cài đặt Python:** Đảm bảo bạn đã cài đặt Python 3.6 trở lên.
2.  **Cài đặt các thư viện:** Mở Terminal hoặc Command Prompt và chạy lệnh sau:
    ```bash
    pip install rembg pillow onnxruntime
    ```

## Cách sử dụng

1.  Lưu mã nguồn vào một file có tên `main.py`.
2.  Mở Terminal hoặc Command Prompt, di chuyển đến thư mục chứa file trên.
3.  Chạy ứng dụng bằng lệnh:
    ```bash
    python main.py
    ```
4.  Làm theo các bước trên giao diện ứng dụng:
    - Nhấn **"1. Chọn Ảnh"** để tải ảnh lên.
    - Nhấn **"2. Tách Nền"** và chờ quá trình xử lý hoàn tất.
    - Nhấn **"3. Lưu Ảnh"** để lưu kết quả.

## Giấy phép

Dự án này được cấp phép theo **Giấy phép MIT**. Xem file `LICENSE` để biết thêm chi tiết.
