class ServiceView:
    @staticmethod
    def show_list(services):
        if not services:
            print("Không có dữ liệu dịch vụ.")
            return
        print("--- DANH SÁCH DỊCH VỤ SAU BÁN HÀNG ---")
        for s in services:
            print(f"ID dịch vụ: {s[0]} | Tên khách hàng: {s[2]} | Xe: {s[4]} | Loại: {s[5]} | Ngày: {s[6].strftime('%Y-%m-%d %H:%M')} | Chi phí: {s[7]:,.0f} | Tên nhân viên: {s[9]} | Trạng thái: {s[10]}")

    @staticmethod
    def show_detail(service):
        if not service:
            print("Không tìm thấy dịch vụ.")
            return
        print("--- CHI TIẾT DỊCH VỤ ---")
        print(f"ID Dịch vụ: {service[0]}")
        print(f"ID Khách hàng: {service[1]} | Tên khách hàng: {service[2]} | SĐT khách hàng: {service[3]}")
        print(f"ID Xe: {service[4]} | Hãng xe: {service[5]}")
        print(f"Loại dịch vụ: {service[6]}")
        service_date = service[7]
        if hasattr(service_date, "strftime"):
            print(f"Ngày dịch vụ: {service_date.strftime('%d/%m/%Y %H:%M')}")
        else:
            print(f"Ngày dịch vụ: {service_date}")
        print(f"Chi phí: {service[8]:,.0f} VNĐ")
        print(f"ID Kỹ thuật viên: {service[9]} | Tên KTV: {service[10]}")
        print(f"Trạng thái: {service[11]}")

    @staticmethod
    def show_customer_selection(customers):
        if not customers:
            print("Không tìm thấy khách hàng nào.")
            return
        print("--- DANH SÁCH KHÁCH HÀNG ---")
        for c in customers:
            print(f"ID khách hàng: {c[0]} | Tên khách hàng: {c[1]} | Số điện thoại: {c[2]}")

    @staticmethod
    def show_vehicle_selection(vehicles):
        if not vehicles:
            print("Không tìm thấy xe nào.")
            return
        print("--- DANH SÁCH XE ---")
        for v in vehicles:
            print(f"ID Xe: {v[0]} | Dòng xe: {v[1]} | Hãng xe: {v[2]} | Năm: {v[3]}")

    @staticmethod
    def show_technician_selection(technicians):
        if not technicians:
            print("Không tìm thấy nhân viên nào.")
            return
        print("--- DANH SÁCH NHÂN VIÊN ---")
        for t in technicians:
            print(f"ID nhân viên: {t[0]} | Tên nhân viên: {t[1]}")

    @staticmethod
    def show_stats(stats):
        if not stats:
            print("Không có dữ liệu thống kê.")
            return
        print("--- THỐNG KÊ DỊCH VỤ THEO TRẠNG THÁI ---")
        for row in stats:
            status = row[0]
            count = row[1]
            print(f"Trạng thái: {status} | Số lượng: {count}")

    @staticmethod
    def show_total_cost_by_service_type(stats):
        if not stats:
            print("Không có dữ liệu thống kê.")
            return
        print("--- TỔNG CHI PHÍ DỊCH VỤ THEO LOẠI ---")
        for row in stats:
            service_type = row[0]
            total_cost = row[1]
            print(f"Loại dịch vụ: {service_type} | Tổng chi phí: {total_cost:,.0f} VNĐ")