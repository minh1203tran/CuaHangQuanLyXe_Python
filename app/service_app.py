import csv
import os
from datetime import datetime, date, time
from controller.service_controller import ServiceController

class ServiceApp:
    def __init__(self):
        self.controller = ServiceController()

    def get_input(self, prompt, default=None, allow_quit=True, to_upper=False, cast_func=None, validation_func=None):
        while True:
            value = input(prompt).strip()
            if allow_quit and value.upper() == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return None
            if not value and default is not None:
                return default
            if to_upper:
                value = value.upper()
            if cast_func:
                try:
                    value = cast_func(value)
                except ValueError:
                    print(f"Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                    continue
            if validation_func:
                if not validation_func(value):
                    continue
            return value

    def select_customer(self):
        while True:
            keyword = self.get_input("Tìm kiếm khách hàng (Tên khách hàng/số điện thoại, 0 để hủy): ")
            if keyword is None: return None
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            customers = self.controller.get_and_show_customers(keyword)
            if not customers:
                continue
            while True:
                customer_id_input = self.get_input("Chọn ID khách hàng (0 để hủy): ", cast_func=int)
                if customer_id_input is None: return None
                selected_customer = next((c for c in customers if c[0] == customer_id_input), None)
                if selected_customer:
                    print(f"Đã chọn khách hàng: {selected_customer[1]} (ID: {selected_customer[0]})")
                    return selected_customer[0]
                else:
                    print("ID khách hàng không hợp lệ. Vui lòng nhập lại!")

    def select_vehicle(self):
        while True:
            keyword = self.get_input("Tìm kiếm hãng xe (0 để hủy): ")
            if keyword is None: return None
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            vehicles = self.controller.get_and_show_vehicles(keyword)
            if not vehicles:
                continue
            while True:
                vehicle_id_input = self.get_input("Chọn ID xe (0 để hủy): ", cast_func=int)
                if vehicle_id_input is None: return None
                selected_vehicle = next((v for v in vehicles if v[0] == vehicle_id_input), None)
                if selected_vehicle:
                    print(f"Đã chọn xe: {selected_vehicle[1]} {selected_vehicle[2]} (ID: {selected_vehicle[0]})")
                    return selected_vehicle[0]
                else:
                    print("ID xe không hợp lệ. Vui lòng nhập lại!")

    def select_technician(self):
        while True:
            keyword = self.get_input("Tìm kiếm tên nhân viên (0 để hủy): ")
            if keyword is None: return None
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            technicians = self.controller.get_and_show_technicians(keyword)
            if not technicians:
                continue
            while True:
                technician_id_input = self.get_input("Chọn ID nhân viên (0 để hủy): ", cast_func=int)
                if technician_id_input is None: return None
                selected_technician = next((t for t in technicians if t[0] == technician_id_input), None)
                if selected_technician:
                    print(f"Đã chọn nhân viên: {selected_technician[1]} (ID: {selected_technician[0]})")
                    return selected_technician[0]
                else:
                    print("ID nhân viên không hợp lệ. Vui lòng nhập lại!")

    def validate_datetime(self, dt_str):
        try:
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Ngày giờ không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD HH:MM.")
            return False
        if dt <= datetime.now():
            print("Ngày giờ dịch vụ phải sau thời điểm hiện tại.")
            return False
        t = dt.time()
        morning_start, morning_end = time(8, 0), time(12, 0)
        afternoon_start, afternoon_end = time(13, 30), time(17, 30)
        if not (morning_start <= t <= morning_end or afternoon_start <= t <= afternoon_end):
            print("Giờ phục vụ chỉ trong 08:00–12:00 hoặc 13:30–17:30.")
            return False
        return True

    # 1. Danh sách dịch vụ
    def hien_thi_ds_service(self):
        self.controller.list_services()

    # 2. Thêm dịch vụ mới
    def them_service_moi(self):
        print("--- THÊM DỊCH VỤ MỚI ---")
        customer_id = self.select_customer()
        if customer_id is None: return
        vehicle_id = self.select_vehicle()
        if vehicle_id is None: return
        while True:
            service_type = self.get_input("Loại dịch vụ (Bảo dưỡng, Sửa chữa, v.v., 0 để hủy): ")
            if service_type is None: return
            if not service_type.strip():
                print("Loại dịch vụ không được để trống. Vui lòng nhập lại!")
                continue
            break
        service_date_str = self.get_input(
            "Ngày giờ dịch vụ (YYYY-MM-DD HH:MM, 0 để hủy): ",
            validation_func=self.validate_datetime
        )
        if service_date_str is None:
            return
        service_date = datetime.strptime(service_date_str, '%Y-%m-%d %H:%M')
        while True:
            cost = self.get_input("Chi phí (VNĐ, 0 để hủy): ", cast_func=float)
            if cost is None:
                return
            if cost < 0:
                print("Chi phí không thể âm. Vui lòng nhập lại!")
                continue
            break
        technician_id = self.select_technician()
        if technician_id is None: return
        status_options = {
            1: "Đang chờ",
            2: "Đang thực hiện",
            3: "Hoàn thành",
            4: "Đã hủy"
        }
        while True:
            print("Chọn trạng thái:")
            for k, v in status_options.items():
                print(f"{k}. {v}")
            status_choice = self.get_input("Nhập số (0 để hủy): ", cast_func=int)
            if status_choice is None: return
            if status_choice in status_options:
                status = status_options[status_choice]
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        result = self.controller.add_service(customer_id, vehicle_id, service_type, service_date, cost, technician_id, status)
        if result:
            print(f"Thêm dịch vụ thành công!")
        else:
            print("Có lỗi xảy ra khi thêm dịch vụ.")

    # 3. Cập nhật dịch vụ
    def cap_nhat_service(self):
        print("--- CẬP NHẬT DỊCH VỤ ---")
        while True:
            keyword = self.get_input("Tìm kiếm dịch vụ theo tên khách hàng/hãng xe/tên nhân viên/loại dịch vụ (0 để hủy): ")
            if keyword is None: return
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            services = self.controller.search_services(keyword)
            if not services:
                print("Không tìm thấy dịch vụ nào. Vui lòng nhập lại.")
                continue
            self.controller.show_service_list(services)
            while True:
                service_id = self.get_input("Chọn ID dịch vụ cần cập nhật (0 để hủy): ", cast_func=int)
                if service_id is None: return
                selected = next((s for s in services if s[0] == service_id), None)
                if not selected:
                    print("ID dịch vụ không có trong danh sách. Vui lòng nhập lại!")
                    continue
                current_service = self.controller.get_service(service_id)
                if not current_service:
                    print("Dịch vụ này không tồn tại trong hệ thống.")
                    continue
                break
            self.controller.show_service_detail(service_id)
            (
                _id, current_customer_id, current_customer_name, current_customer_phone,
                current_vehicle_id, current_vehicle_manufacturer,
                current_service_type, current_service_date, current_cost,
                current_technician_id, current_technician_name,
                current_status
            ) = current_service
            print(f"--- CẬP NHẬT KHÁCH HÀNG (hiện tại: {current_customer_name} - {current_customer_phone}) ---")
            while True:
                raw_input = self.get_input(
                    "Bạn muốn thay đổi khách hàng? (y để đổi, Enter để giữ nguyên, 0 để hủy): ",
                    allow_quit=True,
                    to_upper=True
                )
                if raw_input is None:
                    return
                if raw_input == "":
                    customer_id = current_customer_id
                    break
                if raw_input == "Y":
                    new_customer_id = self.select_customer()
                    if new_customer_id is None: return
                    customer_id = new_customer_id
                    break
                print("Vui lòng chỉ nhập 'y', '0' hoặc Enter.")
            print(f"--- CẬP NHẬT XE (hiện tại: {current_vehicle_manufacturer}) ---")
            while True:
                raw_input = self.get_input(
                    "Bạn muốn thay đổi xe? (y để đổi, Enter để giữ nguyên, 0 để hủy): ",
                    allow_quit=True,
                    to_upper=True
                )
                if raw_input is None:
                    return
                if raw_input == "":
                    vehicle_id = current_vehicle_id
                    break
                if raw_input == "Y":
                    new_vehicle_id = self.select_vehicle()
                    if new_vehicle_id is None:
                        return
                    vehicle_id = new_vehicle_id
                    break
                print("Vui lòng chỉ nhập 'y', '0' hoặc Enter.")
            print(f"--- CẬP NHẬT LOẠI DỊCH VỤ (hiện tại: {current_service_type}) ---")
            service_type = self.get_input("Nhập loại dịch vụ mới (Enter để giữ nguyên, 0 để hủy): ", default=current_service_type)
            if service_type is None: return
            print(f"--- CẬP NHẬT NGÀY GIỜ DỊCH VỤ (hiện tại: {current_service_date.strftime('%Y-%m-%d %H:%M')}) ---")
            new_service_date_str = self.get_input(
                "Nhập ngày giờ dịch vụ mới (YYYY-MM-DD HH:MM, Enter để giữ nguyên, 0 để hủy): ",
                validation_func=self.validate_datetime,
                default=""
            )
            if new_service_date_str is None:
                return
            if new_service_date_str == "":
                service_date = current_service_date
            else:
                service_date = datetime.strptime(new_service_date_str, '%Y-%m-%d %H:%M')
            print(f"--- CẬP NHẬT CHI PHÍ (hiện tại: {current_cost:,.0f} VNĐ) ---")
            while True:
                new_cost_str = self.get_input(
                    "Nhập chi phí mới (Enter để giữ nguyên, 0 để hủy): ",
                    default=""
                )
                if new_cost_str is None: return
                if not new_cost_str.strip():
                    cost = current_cost
                    break
                try:
                    new_cost = float(new_cost_str)
                    if new_cost < 0:
                        print("Chi phí không thể âm. Vui lòng nhập lại!")
                        continue
                    cost = new_cost
                    break
                except ValueError:
                    print("Chi phí không hợp lệ. Vui lòng nhập số.")
            print(f"--- CẬP NHẬT KỸ THUẬT VIÊN (hiện tại: {current_technician_name}) ---")
            while True:
                raw_input = self.get_input(
                    "Bạn muốn thay đổi kỹ thuật viên? (y để đổi, Enter để giữ nguyên, 0 để hủy): ",
                    allow_quit=True,
                    to_upper=True
                )
                if raw_input is None:
                    return
                if raw_input == "":
                    technician_id = current_technician_id
                    break
                if raw_input == "Y":
                    new_technician_id = self.select_technician()
                    if new_technician_id is None:
                        return
                    technician_id = new_technician_id
                    break
                print("Vui lòng chỉ nhập 'y', '0' hoặc Enter.")
            print(f"--- CẬP NHẬT TRẠNG THÁI (hiện tại: {current_status}) ---")
            status_options = {
                1: "Đang chờ",
                2: "Đang thực hiện",
                3: "Hoàn thành",
                4: "Đã hủy"
            }
            while True:
                print("Chọn trạng thái mới (Enter để giữ nguyên, 0 để hủy):")
                for k, v in status_options.items():
                    print(f"{k}. {v}")
                status_input_raw = self.get_input(
                    f"Nhập số (hiện tại: {current_status}): ",
                    allow_quit=True
                )
                if status_input_raw is None:
                    return
                if status_input_raw == "":
                    status = current_status
                    break
                try:
                    status_choice = int(status_input_raw)
                except ValueError:
                    print("Vui lòng nhập số hợp lệ!")
                    continue
                if status_choice in status_options:
                    status = status_options[status_choice]
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            result = self.controller.update_service(
                service_id, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status
            )
            if result:
                print("Cập nhật dịch vụ thành công!")
            else:
                print("Có lỗi xảy ra khi cập nhật dịch vụ.")
            return

    # 4. Xóa dịch vụ
    def xoa_service(self):
        print("--- XÓA DỊCH VỤ ---")
        while True:
            keyword = self.get_input("Tìm kiếm dịch vụ theo tên khách hàng/hãng xe/tên nhân viên/loại dịch vụ để xóa (0 để hủy): ")
            if keyword is None: return
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            services = self.controller.search_services(keyword)
            if not services:
                print("Không tìm thấy dịch vụ nào. Vui lòng nhập lại.")
                continue
            self.controller.show_service_list(services)
            while True:
                service_id = self.get_input("Chọn ID dịch vụ cần xóa (0 để hủy): ", cast_func=int)
                if service_id is None: return
                selected = next((s for s in services if s[0] == service_id), None)
                if not selected:
                    print("ID dịch vụ không có trong danh sách. Vui lòng nhập lại!")
                    continue
                service = self.controller.get_service(service_id)
                if not service:
                    print("Dịch vụ này không tồn tại trong hệ thống.")
                    continue
                break
            self.controller.get_and_show_service_detail(service_id)
            while True:
                confirm = self.get_input("Bạn có chắc chắn muốn xóa dịch vụ này? (y/n): ", to_upper=True)
                if confirm == "Y":
                    result = self.controller.delete_service(service_id)
                    if result:
                        print("Xóa dịch vụ thành công!")
                    else:
                        print("Có lỗi xảy ra khi xóa dịch vụ.")
                    return
                if confirm == "N":
                    print("Hủy thao tác xóa.")
                    return
                print("Vui lòng chỉ nhập 'y', 'n'.")

    # 5. Tìm kiếm dịch vụ
    def tim_kiem_service(self):
        print("--- TÌM KIẾM DỊCH VỤ ---")
        while True:
            keyword = self.get_input("Nhập tên khách hàng/hãng xe/tên nhân viên/loại dịch vụ để tìm kiếm (0 để hủy): ")
            if keyword is None: return
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            services = self.controller.search_services(keyword)
            if not services:
                print("Không tìm thấy dịch vụ nào. Vui lòng nhập lại.")
                continue
            self.controller.show_service_list(services)
            break

    # 6. Xuất báo cáo CSV
    def xuat_csv(self, filename="services_report.csv"):
        output_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
        all_services = self.controller.get_all_services()
        if not all_services:
            print("Không có dữ liệu dịch vụ để xuất CSV.")
            return
        try:
            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID Dịch vụ", "ID Khách hàng", "Tên Khách hàng",
                    "ID Xe", "Hãng Xe", "Loại Dịch vụ", "Ngày Dịch vụ", "Chi phí",
                    "ID nhân viên", "Tên nhân viên", "Trạng thái"
                ])
                for row in all_services:
                    service_id, customer_id, customer_name, \
                        vehicle_id, vehicle_model, \
                        service_type, service_date, cost, \
                        technician_id, technician_name, status = row
                    writer.writerow([
                        service_id, customer_id, customer_name,
                        vehicle_id, vehicle_model,
                        service_type,
                        service_date.strftime('%Y-%m-%d %H:%M') if isinstance(service_date, datetime) else str(
                            service_date),
                        f"{cost:,.0f}",
                        technician_id, technician_name, status
                    ])
            print(f"Xuất báo cáo thành công ra {output_path}")
        except PermissionError:
            print(
                f"Không thể ghi file vào {output_path}. Vui lòng đóng file Excel nếu đang mở.")
        except Exception as e:
            print(f"Lỗi khi xuất CSV: {e}")

    # 7. Lọc theo trạng thái
    def filter_by_status(self):
        status_options = {
            1: "Đang chờ",
            2: "Đang thực hiện",
            3: "Hoàn thành",
            4: "Đã hủy"
        }
        while True:
            print("--- LỌC DỊCH VỤ THEO TRẠNG THÁI ---")
            for k, v in status_options.items():
                print(f"{k}. {v}")
            while True:
                choice = self.get_input("Chọn trạng thái (0 để hủy): ", cast_func=int)
                if choice is None:
                    return
                if choice == 0:
                    return
                if choice not in status_options:
                    print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")
                    continue
                status = status_options[choice]
                break
            services = self.controller.filter_services_by_status(status)
            if not services:
                print(f"Không tìm thấy dịch vụ nào với trạng thái: {status}")
                continue
            self.controller.show_service_list(services)

    # 8. Lọc theo ngày
    def filter_by_date(self):
        print("--- LỌC DỊCH VỤ THEO NGÀY ---")

        def validate_date(date_str):
            try:
                datetime.strptime(date_str, '%Y-%m-%d').date()
                return True
            except ValueError:
                print("Ngày không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")
                return False
        start_date_str = self.get_input("Nhập ngày bắt đầu (YYYY-MM-DD, 0 để hủy): ", validation_func=validate_date)
        if start_date_str is None:
            return
        start_date = datetime.combine(datetime.strptime(start_date_str, '%Y-%m-%d').date(), time.min)
        while True:
            end_date_str = self.get_input("Nhập ngày kết thúc (YYYY-MM-DD, 0 để hủy): ",
                                          validation_func=validate_date)
            if end_date_str is None:
                return
            end_date = datetime.combine(datetime.strptime(end_date_str, '%Y-%m-%d').date(), time.max)
            if end_date < start_date:
                print("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu! Vui lòng nhập lại ngày kết thúc.")
                continue
            break
        services = self.controller.filter_services_by_date(start_date, end_date)
        if not services:
            print(f"Không tìm thấy dịch vụ nào trong khoảng từ {start_date.date()} đến {end_date.date()}.")
            return
        print(f"--- DANH SÁCH DỊCH VỤ (từ {start_date.date()} đến {end_date.date()}) ---")
        self.controller.show_service_list(services)

    # 9. Thống kê dịch vụ
    def stats(self):
        while True:
            print("\n--- THỐNG KÊ DỊCH VỤ ---")
            print("1. Thống kê số lượng theo trạng thái")
            print("2. Thống kê tổng chi phí theo loại dịch vụ")
            print("0. Quay lại")
            while True:
                choice = self.get_input("Chọn loại thống kê (0 để hủy): ", cast_func=int)
                if choice is None or choice == 0:
                    return
                if choice == 1:
                    self.controller.get_service_stats_by_status()
                    break
                elif choice == 2:
                    self.controller.get_service_stats_by_type()
                    break
                else:
                    print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")
                    continue