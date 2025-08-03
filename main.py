# HƯỚNG DẪN CÀI ĐẶT
# 1. Mở Terminal hoặc Command Prompt.
# 2. Chạy các lệnh sau để cài đặt các thư viện cần thiết:
#    pip install rembg
#    pip install pillow
#    pip install onnxruntime

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove
import threading
import io

class BackgroundRemoverApp:
    def __init__(self, root):
        """
        Hàm khởi tạo giao diện chính của ứng dụng.
        """
        self.root = root
        self.root.title("Phần mềm Tách nền Ảnh")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Biến lưu trữ đường dẫn và dữ liệu ảnh
        self.input_path = None
        self.output_image = None

        # --- Tạo các khung giao diện ---
        # Khung chứa các nút điều khiển
        control_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
        control_frame.pack(fill=tk.X)

        # Khung chứa 2 ảnh (gốc và kết quả)
        image_frame = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10)
        image_frame.pack(fill=tk.BOTH, expand=True)
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(1, weight=1)

        # --- Tạo các widget (nút, nhãn,...) ---
        # Nút chọn ảnh
        self.btn_select = tk.Button(control_frame, text="1. Chọn Ảnh", command=self.select_image, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10)
        self.btn_select.pack(side=tk.LEFT, padx=10)

        # Nút tách nền
        self.btn_remove = tk.Button(control_frame, text="2. Tách Nền", command=self.start_remove_background_thread, state=tk.DISABLED, font=("Helvetica", 12), bg="#f44336", fg="white", relief=tk.FLAT, padx=10)
        self.btn_remove.pack(side=tk.LEFT, padx=10)

        # Nút lưu ảnh
        self.btn_save = tk.Button(control_frame, text="3. Lưu Ảnh", command=self.save_image, state=tk.DISABLED, font=("Helvetica", 12), bg="#2196F3", fg="white", relief=tk.FLAT, padx=10)
        self.btn_save.pack(side=tk.LEFT, padx=10)

        # Nhãn trạng thái
        self.status_label = tk.Label(control_frame, text="Vui lòng chọn một ảnh để bắt đầu", font=("Helvetica", 10), bg="#f0f0f0")
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Khu vực hiển thị ảnh
        tk.Label(image_frame, text="Ảnh Gốc", font=("Helvetica", 14, "bold"), bg="#e0e0e0").grid(row=0, column=0, pady=5)
        self.original_image_label = tk.Label(image_frame, bg="#ffffff", relief=tk.SUNKEN, borderwidth=1)
        self.original_image_label.grid(row=1, column=0, sticky="nsew", padx=5)

        tk.Label(image_frame, text="Kết Quả", font=("Helvetica", 14, "bold"), bg="#e0e0e0").grid(row=0, column=1, pady=5)
        self.result_image_label = tk.Label(image_frame, bg="#ffffff", relief=tk.SUNKEN, borderwidth=1)
        self.result_image_label.grid(row=1, column=1, sticky="nsew", padx=5)

    def select_image(self):
        """
        Mở hộp thoại để người dùng chọn một file ảnh.
        """
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if path:
            self.input_path = path
            self.status_label.config(text="Đã chọn ảnh. Sẵn sàng tách nền.")
            
            # Hiển thị ảnh gốc
            img = Image.open(self.input_path)
            self.display_image(img, self.original_image_label)
            
            # Kích hoạt nút tách nền
            self.btn_remove.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.DISABLED) # Vô hiệu hóa nút lưu khi chọn ảnh mới
            self.result_image_label.config(image='') # Xóa ảnh kết quả cũ


    def start_remove_background_thread(self):
        """
        Tạo một luồng mới để xử lý tách nền, tránh làm treo giao diện.
        """
        if not self.input_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn một ảnh trước!")
            return
        
        # Vô hiệu hóa các nút trong khi xử lý
        self.btn_select.config(state=tk.DISABLED)
        self.btn_remove.config(state=tk.DISABLED)
        self.status_label.config(text="Đang xử lý, vui lòng chờ...")
        
        # Tạo và bắt đầu luồng xử lý
        processing_thread = threading.Thread(target=self.remove_background)
        processing_thread.start()

    def remove_background(self):
        """
        Hàm chính để thực hiện việc tách nền bằng thư viện rembg.
        """
        try:
            with open(self.input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)
                
                # Lưu kết quả vào biến self.output_image
                self.output_image = Image.open(io.BytesIO(output_data))
                
                # Hiển thị ảnh kết quả lên giao diện
                self.display_image(self.output_image, self.result_image_label)
                
                # Cập nhật trạng thái và kích hoạt các nút
                self.status_label.config(text="Hoàn tất! Bạn có thể lưu ảnh.")
                self.btn_save.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Lỗi Xử Lý", f"Đã có lỗi xảy ra: {e}")
            self.status_label.config(text="Xử lý thất bại.")
        finally:
            # Kích hoạt lại các nút sau khi xử lý xong (dù thành công hay thất bại)
            self.btn_select.config(state=tk.NORMAL)
            self.btn_remove.config(state=tk.NORMAL)


    def save_image(self):
        """
        Mở hộp thoại để người dùng lưu ảnh đã tách nền.
        """
        if self.output_image:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            if save_path:
                self.output_image.save(save_path)
                messagebox.showinfo("Thành Công", f"Đã lưu ảnh tại: {save_path}")
                self.status_label.config(text="Đã lưu ảnh thành công.")
        else:
            messagebox.showwarning("Cảnh báo", "Không có ảnh kết quả để lưu.")

    def display_image(self, img, label):
        """
        Hiển thị một ảnh PIL lên một widget Label của Tkinter.
        """
        # Lấy kích thước của khung chứa ảnh
        label.update_idletasks()
        max_width = label.winfo_width() - 10
        max_height = label.winfo_height() - 10

        # Thay đổi kích thước ảnh để vừa với khung
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Chuyển đổi sang định dạng của Tkinter và hiển thị
        photo_img = ImageTk.PhotoImage(img)
        label.config(image=photo_img)
        label.image = photo_img # Giữ tham chiếu để ảnh không bị xóa bởi garbage collector


if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
