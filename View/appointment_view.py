class AppointmentView:
    @staticmethod
    def show_list(appointments):
        if not appointments:
            print("Không có dữ liệu lịch hẹn.")
            return
        print("--- DANH SÁCH LỊCH HẸN ---")
        for a in appointments:
            print(f"ID lịch hẹn: {a[0]} | Tên khách hàng: {a[2]} ({a[3]}) | Mục đích: {a[4]} | Ngày: {a[5]} | "
                  f"Trạng thái: {a[6]}")

    @staticmethod
    def show_detail(appointment):
        if not appointment:
            print("Không tìm thấy lịch hẹn.")
            return
        print("--- CHI TIẾT LỊCH HẸN ---")
        print(f"ID lịch hẹn: {appointment[0]}")
        print(f"ID khách hàng: {appointment[1]}")
        print(f"Tên khách hàng: {appointment[2]}")
        print(f"số điện thoại: {appointment[3]}")
        print(f"Mục đích: {appointment[4]}")
        print(f"Ngày hẹn: {appointment[5].strftime('%d/%m/%Y')}")
        print(f"Trạng thái: {appointment[6]}")

    @staticmethod
    def show_customer_selection(customers):
        if not customers:
            print("Không tìm thấy khách hàng nào.")
            return
        print("--- DANH SÁCH KHÁCH HÀNG ---")
        for c in customers:
            print(f"ID khách hàng: {c[0]} | Tên khách hàng: {c[1]} | Số điện thoại: {c[2]}")