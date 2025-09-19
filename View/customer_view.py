class CustomerView:
    @staticmethod
    def show_customer_list(customers):
        if not customers:
            print("--- Không có dữ liệu khách hàng ---")
            return
        print("--- Danh Sách Khách Hàng ---")
        for c in customers:
            print(f"ID: {c[0]} | Username: {c[1]} | Họ tên: {c[2]} | Email: {c[3]} | "
                  f"Phone: {c[4]} | Địa chỉ: {c[5]} | CCCD: {c[6]} | Ngày tạo: {c[7]} | Trạng thái: {'Hoạt động' if c[8]==1 else 'Khóa'}")

    @staticmethod
    def show_customer_detail(c):
        if not c:
            print("Không tìm thấy khách hàng!")
            return
        print("\n--- THÔNG TIN KHÁCH HÀNG ---")
        print(f"ID: {c[0]}")
        print(f"Username: {c[1]}")
        print(f"Họ tên: {c[2]}")
        print(f"Email: {c[3]}")
        print(f"Phone: {c[4]}")
        print(f"Địa chỉ: {c[5]}")
        print(f"CCCD: {c[6]}")
        print(f"Ngày tạo: {c[7]}")
        print(f"Trạng thái: {'Hoạt động' if c[8]==1 else 'Khóa'}")

    @staticmethod
    def show_statistics(total, active, locked):
        print("\n--- THỐNG KÊ CUSTOMER ---")
        print(f"Tổng số khách hàng: {total}")
        print(f"Đang hoạt động: {active}")
        print(f"Đã khóa: {locked}")

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_error(err):
        print(f"Lỗi: {err}")
