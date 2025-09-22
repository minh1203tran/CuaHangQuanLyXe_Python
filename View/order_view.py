class OrderView:
    @staticmethod
    def show_orders(orders):
        if not orders:
            print("--- Không có đơn hàng ---")
            return
        print("--- DANH SÁCH ĐƠN HÀNG ---")
        for o in orders:
            print(f"ID: {o[0]} | khách hàng: {o[2]} | nhân viên: {o[4]} | Ngày: {o[5]} | "
                  f"Tổng: {o[6]} | Trạng thái: {o[7]} | Thanh toán: {o[8]} | Địa chỉ: {o[9]} | Ghi chú: {o[10]}")

    @staticmethod
    def show_order_details(details):
        if not details:
            print("--- Không có chi tiết đơn ---")
            return
        print("--- CHI TIẾT ĐƠN HÀNG ---")
        for d in details:
            print(f"ID chi tiết: {d[0]} | ID xe: {d[1]} | Dòng xe: {d[2]} | số lượng: {d[3]} | "
                  f"Đơn giá: {d[4]} | Tổng tiền: {d[5]}")

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_error(err):
        print(f"Lỗi: {err}")
