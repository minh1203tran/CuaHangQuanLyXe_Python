import csv
import os
from datetime import datetime, date, time
from controller.appointment_controller import AppointmentController


class AppointmentApp:
    def __init__(self):
        self.controller = AppointmentController()

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
                    print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                    continue
            if validation_func:
                if not validation_func(value):
                    continue
            return value

    def select_customer(self):
        while True:
            keyword = self.get_input("Tìm kiếm khách hàng (tên/số điện thoại, 0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return None
            if not keyword.strip():
                print("Từ khóa không được để trống. Vui lòng nhập lại!")
                continue
            customers = self.controller.get_and_show_customers(keyword)
            if not customers:
                continue
            while True:
                customer_id_input = self.get_input("Chọn ID khách hàng (0 để hủy): ", cast_func=int)
                if customer_id_input is None or customer_id_input == 0:
                    return None
                selected_customer = next((c for c in customers if c[0] == customer_id_input), None)
                if selected_customer:
                    print(f"Đã chọn khách hàng: {selected_customer[1]} (ID: {selected_customer[0]})")
                    return selected_customer[0]
                else:
                    print("ID khách hàng không hợp lệ. Vui lòng nhập lại!")

    # 1. Danh sách lịch hẹn
    def hien_thi_ds_appointment(self):
        self.controller.list_appointments()

    # 2. Thêm lịch hẹn mới
    def them_appointment_moi(self):
        print("--- THÊM LỊCH HẸN MỚI ---")
        customer_id = self.select_customer()
        if customer_id is None:
            return
        while True:
            purpose = self.get_input("Mục đích hẹn (Xem xe, Bảo dưỡng, v.v., 0 để hủy): ")
            if purpose is None or purpose.strip() == "0":
                return None
            if not purpose.strip():
                print("Mục đích hẹn không được để trống. Vui lòng nhập lại!")
                continue
            break
        def validate_date(date_str):
            try:
                datetime.strptime(date_str, '%Y-%m-%d').date()
                return True
            except ValueError:
                print("Ngày không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")
                return False
        while True:
            appointment_date_str = self.get_input("Nhập ngày hẹn (YYYY-MM-DD, 0 để hủy): ", validation_func=validate_date)
            if appointment_date_str is None:
                return
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
            if appointment_date < date.today():
                print("Ngày hẹn không thể trong quá khứ! Vui lòng nhập lại.")
                continue
            break
        def validate_time(time_str):
            try:
                t = datetime.strptime(time_str, '%H:%M').time()
                morning_start = time(8, 0)
                morning_end = time(12, 0)
                afternoon_start = time(13, 30)
                afternoon_end = time(17, 30)
                if (morning_start <= t <= morning_end) or (afternoon_start <= t <= afternoon_end):
                    return True
                else:
                    print("Giờ hẹn phải trong khung 08:00-12:00 hoặc 13:30-17:30.")
                    return False
            except ValueError:
                print("Giờ không hợp lệ! Vui lòng nhập theo định dạng HH:MM.")
                return False
        while True:
            appointment_time_str = self.get_input("Nhập giờ hẹn (HH:MM, 0 để hủy): ", validation_func=validate_time)
            if appointment_time_str is None:
                return
            appointment_time = datetime.strptime(appointment_time_str, '%H:%M').time()
            break
        status_options = {
            1: "Đã xác nhận",
            2: "Hoàn thảnh",
            3: "Đã hủy"
        }
        while True:
            print("Chọn trạng thái:")
            for k, v in status_options.items():
                print(f"{k}. {v}")
            status_choice = self.get_input("Nhập số (0 để hủy): ", cast_func=int)
            if status_choice is None:
                return
            if status_choice in status_options:
                status = status_options[status_choice]
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        result = self.controller.add_appointment(customer_id, purpose, appointment_date, appointment_time, status)
        if result:
            print(f"Thêm lịch hẹn thành công!")
        else:
            print("Có lỗi xảy ra khi thêm lịch hẹn.")

    # 3. Cập nhật lịch hẹn
    def cap_nhat_appointment(self):
        print("--- CẬP NHẬT LỊCH HẸN ---")
        while True:
            keyword = self.get_input("Tìm kiếm lịch hẹn theo tên khách hàng/số điện thoại (0 để hủy): ")
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập tên khách hàng hoặc số điện thoại!")
                continue
            appointments = self.controller.search_appointments(keyword)
            if not appointments:
                print("Không tìm thấy lịch hẹn nào. Vui lòng nhập lại.")
                continue
            self.controller.show_appointments(appointments)
            while True:
                appointment_id = self.get_input("Chọn ID lịch hẹn cần cập nhật (0 để hủy): ", cast_func=int)
                if appointment_id is None or appointment_id == 0:
                    return
                selected = next((a for a in appointments if a[0] == appointment_id), None)
                if not selected:
                    print("ID lịch hẹn không có trong danh sách. Vui lòng nhập lại!")
                    continue
                current_appointment = self.controller.get_appointment(appointment_id)
                if not current_appointment:
                    print("Lịch hẹn này không tồn tại trong hệ thống.")
                    continue
                break
            self.controller.get_and_show_appointment_detail(appointment_id)
            _id, current_customer_id, current_customer_name, current_customer_phone, \
                current_purpose, current_datetime, current_status = current_appointment
            current_date = current_datetime.date()
            current_time = current_datetime.time()
            print(f"--- CẬP NHẬT KHÁCH HÀNG (hiện tại: {current_customer_name} - {current_customer_phone}) ---")
            while True:
                raw_input = input(
                    "Bạn muốn thay đổi khách hàng? (y để đổi, Enter để giữ nguyên, 0 để hủy): ").strip().upper()
                if raw_input == "0":
                    print("Hủy thao tác cập nhật, quay lại menu chính!")
                    return
                if raw_input == "":
                    customer_id = current_customer_id
                    break
                if raw_input == "Y":
                    new_customer_id = self.select_customer()
                    if new_customer_id is None:
                        return
                    customer_id = new_customer_id
                    break
                print("Vui lòng chỉ nhập 'y', '0' hoặc Enter.")
            print(f"--- CẬP NHẬT MỤC ĐÍCH (hiện tại: {current_purpose}) ---")
            purpose = self.get_input("Nhập mục đích mới (Enter để giữ nguyên, 0 để hủy): ", default=current_purpose)
            if purpose is None: return
            def validate_date(date_str):
                try:
                    d = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if d < date.today():
                        print("Ngày hẹn không thể trong quá khứ! Vui lòng nhập lại.")
                        return False
                    return True
                except ValueError:
                    print("Ngày không hợp lệ! Vui lòng nhập theo định dạng YYYY-MM-DD.")
                    return False
            print(f"--- CẬP NHẬT NGÀY HẸN (hiện tại: {current_date.strftime('%Y-%m-%d')}) ---")
            while True:
                new_date_str = self.get_input(
                    "Nhập ngày hẹn mới (YYYY-MM-DD, Enter để giữ nguyên, 0 để hủy): ",
                    validation_func=validate_date,
                    default=""
                )
                if new_date_str is None or new_date_str == "0":
                    return
                if new_date_str.strip() == "":
                    appointment_date = current_date
                    break
                appointment_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                break
            def validate_time(time_str):
                try:
                    t = datetime.strptime(time_str, '%H:%M').time()
                except ValueError:
                    print("Giờ không hợp lệ! Vui lòng nhập theo định dạng HH:MM.")
                    return False
                morning_start = datetime.strptime("08:00", "%H:%M").time()
                morning_end = datetime.strptime("12:00", "%H:%M").time()
                afternoon_start = datetime.strptime("13:30", "%H:%M").time()
                afternoon_end = datetime.strptime("17:30", "%H:%M").time()
                if (morning_start <= t <= morning_end) or (afternoon_start <= t <= afternoon_end):
                    return True
                print("Giờ hẹn chỉ được trong khoảng 08:00–12:00 hoặc 13:30–17:30.")
                return False
            print(f"--- CẬP NHẬT GIỜ HẸN (hiện tại: {current_time.strftime('%H:%M')}) ---")
            new_time_str = self.get_input(
                "Nhập giờ hẹn mới (HH:MM, Enter để giữ nguyên, 0 để hủy): ",
                validation_func=validate_time, default=""
            )
            if new_time_str is None or new_time_str == "0":
                return
            appointment_time = datetime.strptime(new_time_str, '%H:%M').time() if new_time_str else current_time
            print(f"--- CẬP NHẬT TRẠNG THÁI (hiện tại: {current_status}) ---")
            status_options = {
                1: "Đã xác nhận",
                2: "Hoàn thành",
                3: "Đã hủy"
            }
            while True:
                print("Chọn trạng thái mới (Enter để giữ nguyên, 0 để hủy):")
                for k, v in status_options.items():
                    print(f"{k}. {v}")
                status_input_raw = input(f"Nhập số (hiện tại: {current_status}): ").strip()
                if status_input_raw == "0":
                    print("Hủy thao tác cập nhật.")
                    return
                if not status_input_raw:
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
            result = self.controller.update_appointment(
                appointment_id, customer_id, purpose, appointment_date, appointment_time, status
            )
            if result:
                print("Cập nhật lịch hẹn thành công!")
            else:
                print("Có lỗi xảy ra khi cập nhật lịch hẹn.")
            return

    # 4. Xóa lịch hẹn
    def xoa_appointment(self):
        print("--- XÓA LỊCH HẸN ---")
        while True:
            keyword = self.get_input("Tìm kiếm lịch hẹn theo tên khách hàng/số điện thoại để xóa (0 để hủy): ")
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập tên khách hàng hoặc số điện thoại!")
                continue
            appointments = self.controller.search_appointments(keyword)
            if not appointments:
                print("Không tìm thấy lịch hẹn nào. Vui lòng nhập lại.")
                continue
            self.controller.show_appointments(appointments)
            while True:
                appointment_id = self.get_input("Chọn ID lịch hẹn cần xóa (0 để hủy): ", cast_func=int)
                if appointment_id is None or appointment_id == 0:
                    return
                selected = next((a for a in appointments if a[0] == appointment_id), None)
                if not selected:
                    print("ID lịch hẹn không có trong danh sách. Vui lòng nhập lại!")
                    continue
                appointment = self.controller.get_appointment(appointment_id)
                if not appointment:
                    print("Lịch hẹn này không tồn tại trong hệ thống.")
                    continue
                break
            self.controller.get_and_show_appointment_detail(appointment_id)
            while True:
                confirm = self.get_input(
                    "Bạn có chắc chắn muốn xóa lịch hẹn này? (y/n): ",
                    to_upper=True
                )
                if confirm is None:
                    continue
                if confirm == "Y":
                    result = self.controller.delete_appointment(appointment_id)
                    if result:
                        print("Xóa lịch hẹn thành công!")
                    else:
                        print("Có lỗi xảy ra khi xóa lịch hẹn.")
                    return
                if confirm == "N":
                    print("Hủy thao tác xóa.")
                    return
                print("Vui lòng chỉ nhập 'y', 'n' hoặc '0'.")

    # 5. Tìm kiếm lịch hẹn
    def tim_kiem_appointment(self):
        print("--- TÌM KIẾM LỊCH HẸN ---")
        while True:
            keyword = self.get_input("Nhập tên khách hàng hoặc số điện thoại để tìm kiếm (0 để hủy): ")
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập tên khách hàng hoặc số điện thoại!")
                continue
            appointments = self.controller.search_appointments(keyword)
            if not appointments:
                print("Không tìm thấy lịch hẹn nào. Vui lòng nhập lại.")
                continue
            self.controller.show_appointments(appointments)
            break

    # 6. Xuất báo cáo CSV
    def xuat_csv(self, filename="appointments_report.csv"):
        output_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
        all_appointments = self.controller.model.get_all()
        if not all_appointments:
            print("Không có dữ liệu lịch hẹn để xuất CSV.")
            return
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID lịch hẹn", "ID khách hàng", "Tên khách hàng", "Số điện thoại",
                "Mục đích", "Ngày hẹn", "Giờ hẹn", "Trạng thái"
            ])
            for row in all_appointments:
                row_list = list(row)
                appointment_dt = row_list[5]
                if isinstance(appointment_dt, datetime):
                    ngay = appointment_dt.strftime('%Y-%m-%d')
                    gio = appointment_dt.strftime('%H:%M')
                else:
                    ngay = str(appointment_dt) if appointment_dt else ""
                    gio = ""
                row_list[5] = ngay
                row_list.insert(6, gio)
                writer.writerow(row_list)
        print(f"Xuất báo cáo thành công ra {output_path}")

    # 7. Lọc theo trạng thái
    def filter_by_status(self):
        status_options = {
            1: "Đã xác nhận",
            2: "Hoàn thành",
            3: "Đã hủy"
        }
        print("--- LỌC LỊCH HẸN THEO TRẠNG THÁI ---")
        for k, v in status_options.items():
            print(f"{k}. {v}")
        print("0. Quay lại")
        while True:
            choice = self.get_input("Chọn trạng thái: ", cast_func=int)
            if choice is None or choice == 0:
                return
            status = status_options.get(choice)
            if not status:
                print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")
                continue
            appointments = self.controller.filter_appointments_by_status(status)
            if not appointments:
                print(f"Không tìm thấy lịch hẹn nào với trạng thái: {status}")
                continue
            print(f"--- DANH SÁCH LỊCH HẸN ({status}) ---")
            for a in appointments:
                print(f"ID lịch hẹn: {a[0]} | "
                      f"Tên khách hàng: {a[2]} ({a[3]}) | "
                      f"Mục đích: {a[4]} | "
                      f"Ngày: {a[5]} | "
                      f"Trạng thái: {a[6]}")
            print("--- LỌC LỊCH HẸN THEO TRẠNG THÁI ---")
            for k, v in status_options.items():
                print(f"{k}. {v}")
            print("0. Quay lại")

    # 8. Lọc theo ngày
    def filter_by_date(self):
        print("--- LỌC LỊCH HẸN THEO NGÀY ---")
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
            end_date_str = self.get_input("Nhập ngày kết thúc (YYYY-MM-DD, 0 để hủy): ", validation_func=validate_date)
            if end_date_str is None:
                return
            end_date = datetime.combine(datetime.strptime(end_date_str, '%Y-%m-%d').date(), time.max)
            if end_date < start_date:
                print("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu! Vui lòng nhập lại ngày kết thúc.")
                continue
            break
        appointments = self.controller.filter_appointments_by_date(start_date, end_date)
        if not appointments:
            print(f"Không tìm thấy lịch hẹn nào trong khoảng từ {start_date} đến {end_date}.")
            return
        print(f"--- DANH SÁCH LỊCH HẸN (từ {start_date.date()} đến {end_date.date()}) ---")
        for a in appointments:
            print(f"ID lịch hẹn: {a[0]} | "
                  f"Tên khách hàng: {a[2]} ({a[3]}) | "
                  f"Mục đích: {a[4]} | "
                  f"Ngày: {a[5].date()} | "
                  f"Trạng thái: {a[6]}")

    # 9. Thống kê lịch hẹn
    def stats(self):
        stats = self.controller.get_appointment_stats()
        if not stats:
            print("Không có dữ liệu thống kê.")
            return
        print("--- THỐNG KÊ LỊCH HẸN THEO TRẠNG THÁI ---")
        for row in stats:
            status = row[0]
            count = row[1]
            print(f"Trạng thái: {status} | Số lượng: {count}")
