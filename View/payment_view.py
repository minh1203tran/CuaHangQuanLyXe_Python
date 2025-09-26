class PaymentView:
    @staticmethod
    def show_list(payments):
        if not payments:
            print("Không có dữ liệu thanh toán.")
            return
        print("--- DANH SÁCH THANH TOÁN ---")
        for p in payments:
            print(f"ID Thanh toán: {p[0]} | ID đơn hàng: {p[1]} | Số tiền: {p[2]} | Ngày: {p[3]} "
                  f"| Phương thức: {p[4]} | Transaction: {p[5]} | Trạng thái: {p[6]}")

    @staticmethod
    def show_detail(payment):
        if not payment:
            print("Không tìm thấy thanh toán.")
            return
        print("--- CHI TIẾT THANH TOÁN ---")
        print(f"ID thanh toán: {payment[0]}")
        print(f"ID đơn hàng: {payment[1]}")
        print(f"Tên khách hàng: {payment[2]}")
        print(f"Số điện thoại: {payment[3]}")
        print(f"Số tiền: {payment[4]:,.0f}")
        print(f"Phương thức: {payment[5]}")
        print(f"Transaction ID: {payment[6]}")
        print(f"Trạng thái: {payment[7]}")
        print(f"Ngày: {payment[8]}")