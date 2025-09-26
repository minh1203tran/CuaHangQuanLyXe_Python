import re
import datetime
from controller.vehicle_controller import VehicleController

class VehicleApp:
    def __init__(self):
        self.controller = VehicleController()

    def get_input(self, prompt, default=None, allow_quit=True, to_upper=False, validator=None, cast_func=None):
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
            if validator and not validator(value):
                print("Giá trị không hợp lệ! Vui lòng nhập lại.")
                continue
            return value

    # 1. Danh sách tất cả xe
    def hien_thi_ds_xe(self):
        self.controller.list_vehicles()

    # Validate biển số xe
    def validate_license_plate(self, lp: str) -> bool:
        pattern = r'^(\d{2}-[A-Z]{1,2}\d{1}-\d{5}|\d{2}[A-Z]{1}-\d{5})$'
        return re.match(pattern, lp) is not None

    # 2. Thêm xe
    def them_xe_moi(self):
        print("--- Thêm thông tin mới (Nhấn 0 để hủy thao tác này) ---")
        while True:
            raw_lp = self.get_input("Biển số 'VD:34F-67439' (Enter để bỏ qua): ", cast_func=str, allow_quit=True)
            if raw_lp is None:
                return
            if raw_lp == "":
                lp = None
                break
            lp = raw_lp.upper()
            if not self.validate_license_plate(lp):
                print("Biển số không hợp lệ! Vui lòng nhập lại.")
                continue
            if self.controller.check_license_plate_exists(lp):
                print("Biển số đã tồn tại trong hệ thống! Vui lòng nhập lại.")
                continue
            break
        while True:
            model = self.get_input("Dòng xe: ", cast_func=str)
            if model is None:
                return
            if not model.strip():
                print("Dòng xe là bắt buộc! Vui lòng nhập lại.")
                continue
            break
        while True:
            manu = self.get_input("Hãng: ", cast_func=str)
            if manu is None:
                return
            if not manu.strip():
                print("Hãng xe là bắt buộc! Vui lòng nhập lại.")
                continue
            break
        while True:
            year = self.get_input("Năm SX: ", cast_func=int)
            if year is None:
                return
            if year > 2025:
                print("Năm sản xuất phải bé hơn hoặc bằng năm hiện tại!")
                continue
            break
        while True:
            price = self.get_input("Giá xe (VNĐ): ", cast_func=float)
            if price is None:
                return
            if price <= 0:
                print("Giá xe phải lớn hơn 0! Vui lòng nhập lại.")
                continue
            break
        self.controller.add_vehicle(lp, model, manu, year, price)

    # 3. Cập nhật thông tin xe
    def cap_nhat_xe(self):
        while True:
            manu_search = self.get_input("Nhập tên hãng xe để tìm (0 để hủy): ", cast_func=str)
            if manu_search is None:
                print("Bạn phải nhập tên hãng xe!")
                continue
            manu_search = manu_search.strip()
            if manu_search == "0":
                return
            if manu_search == "":
                print("Bạn phải nhập tên hãng xe!")
                continue
            vehicles = self.controller.model.search_by_manufacturer(manu_search)
            if not vehicles:
                print("Không tìm thấy xe nào. Vui lòng thử lại.")
                continue
            break
        print("KẾT QUẢ TÌM KIẾM")
        for v in vehicles:
            price_val = v[6] if v[6] is not None else 0  # cột giá đúng
            print(f"ID: {v[0]} | Biển số: {v[1]} | Dòng: {v[2]} | Hãng: {v[3]} | "
                  f"Năm: {v[4]} | Giá: {int(price_val):,} VNĐ")
        valid_ids = [v[0] for v in vehicles]
        while True:
            vid = self.get_input("Nhập ID xe cần cập nhật (0 để hủy): ", cast_func=int)
            if vid is None or vid == 0:
                return
            if vid not in valid_ids:
                print("ID không hợp lệ! Vui lòng chọn ID trong danh sách vừa tìm được.")
                continue
            current_vehicle = next(v for v in vehicles if v[0] == vid)
            break
        print("Nhập thông tin mới (Enter để giữ nguyên, 0 để hủy)")
        while True:
            raw_lp = input(f"Biển số mới [Hiện tại: {current_vehicle[1]}]: ").strip().upper()
            if raw_lp == "0":
                return
            lp = raw_lp if raw_lp != "" else current_vehicle[1]
            if lp != current_vehicle[1] and not self.validate_license_plate(lp):
                print("Biển số không hợp lệ! Vui lòng nhập lại.")
                continue
            break
        model = self.get_input("Dòng xe mới: ", default=current_vehicle[2])
        if model is None:
            return
        manu = self.get_input("Hãng mới: ", default=current_vehicle[3])
        if manu is None:
            return
        current_year = datetime.datetime.now().year
        while True:
            raw_year = input(f"Năm SX mới [Hiện tại: {current_vehicle[4]}]: ").strip()
            if raw_year == "0":  # hủy
                return
            if raw_year == "":
                year = current_vehicle[4]
                break
            try:
                year = int(raw_year)
                if year < 1900 or year > current_year:
                    print(f"Năm không hợp lệ! Vui lòng nhập từ 1900 đến {current_year}.")
                    continue
                break
            except ValueError:
                print("Nhập sai định dạng! Vui lòng nhập lại.")
        current_price = current_vehicle[6] if current_vehicle[6] is not None else 0
        while True:
            try:
                raw_price = input(f"Giá xe mới (VNĐ) [Hiện tại: {int(current_price):,}]: ").strip()
                if raw_price == "0":  # hủy
                    return
                if raw_price == "":
                    price_input = current_price
                else:
                    price_input = float(raw_price)
                    if price_input <= 0:
                        print("Giá xe phải lớn hơn 0! Vui lòng nhập lại.")
                        continue
                break
            except ValueError:
                print("Nhập sai định dạng! Vui lòng nhập lại.")
        while True:
            confirm = input("Bạn có chắc chắn muốn cập nhật xe này? (Y/N): ").strip().upper()
            if confirm == "Y":
                self.controller.update_vehicle(vid, lp, model, manu, year, price_input)
                break
            elif confirm == "N":
                print("Hủy cập nhật xe.")
                break
            else:
                print("Vui lòng nhập Y hoặc N!")

    # 4. Xóa xe
    def xoa_xe(self):
        while True:
            manu_search = input("Nhập tên hãng xe để tìm (0 để hủy): ").strip()
            if manu_search == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return
            if manu_search == "":
                print("Bạn phải nhập tên hãng xe!")
                continue

            vehicles = self.controller.model.search_by_manufacturer(manu_search)
            if not vehicles:
                print("Không tìm thấy xe nào. Vui lòng thử lại.")
                continue
            break

        print("KẾT QUẢ TÌM KIẾM")
        for v in vehicles:
            price_val = v[6] if v[6] is not None else 0
            print(f"ID: {v[0]} | Biển số: {v[1]} | Dòng: {v[2]} | Hãng: {v[3]} | "
                  f"Năm: {v[4]} | Giá: {int(price_val):,} VNĐ")

        valid_ids = [v[0] for v in vehicles]

        while True:
            vid_input = input("Nhập ID xe cần xóa (0 để hủy): ").strip()
            if vid_input == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return
            try:
                vid = int(vid_input)
            except ValueError:
                print("Vui lòng nhập số hợp lệ!")
                continue
            if vid not in valid_ids:
                print("ID không hợp lệ! Vui lòng chọn ID trong danh sách vừa tìm được.")
                continue
            break

        while True:
            confirm = input(f"Bạn có chắc chắn muốn xóa xe với ID {vid}? (Y/N): ").strip().upper()
            if confirm == "Y":
                self.controller.delete_vehicle(vid)
                break
            elif confirm == "N":
                print("Hủy thao tác xóa, quay lại menu chính!")
                break
            else:
                print("Vui lòng nhập Y hoặc N!")

    # 5. Lấy thông tin xe theo ID
    def xem_chi_tiet_xe(self):
        print("--- DANH SÁCH XE ---")
        vehicles = self.controller.model.get_all()
        if not vehicles:
            print("Không có xe nào trong hệ thống!")
            return
        for v in vehicles:
            price_val = v[6] if v[6] is not None else 0
            print(
                f"ID: {v[0]} | Biển số: {v[1]} | Dòng: {v[2]} | Hãng: {v[3]} | Năm: {v[4]} | Giá: {int(price_val):,} VNĐ")
        while True:
            vid = self.get_input("Nhập ID xe để xem chi tiết (0 để hủy): ", cast_func=int)
            if vid is None:
                return
            vehicle_exists = any(v[0] == vid for v in vehicles)
            if vehicle_exists:
                self.controller.get_vehicle_by_id(vid)
                break
            else:
                print("ID không có trong danh sách! Vui lòng nhập lại hoặc nhập 0 để hủy.")
                continue

    # 6. Tìm kiếm theo hãng
    def tim_theo_hang(self):
        while True:
            manu = self.get_input("Nhập tên hãng xe (0 để hủy): ", cast_func=str)
            if manu is None or manu.strip() == "0":
                break
            vehicles = self.controller.search_by_manufacturer(manu)
            if vehicles:
                print("--- KẾT QUẢ TÌM KIẾM ---")
                for v in vehicles:
                    print(f"ID: {v[0]} | Biển số xe: {v[1]} | Dòng xe: {v[2]} | Hãng xe: {v[3]} | "
                          f"Năm SX: {v[4]} | Ngày tạo: {v[5]} | Giá: {v[6]:,} VNĐ")
                break
            else:
                print("Không tìm thấy xe nào. Vui lòng thử lại hoặc nhập 0 để thoát.")

    # 7. Tìm kiếm theo năm sản xuất
    def tim_theo_nam(self):
        while True:
            year = self.get_input("Nhập năm sản xuất (0 để hủy): ", cast_func=int)
            if year is None:
                return
            if year <= 0 or year > 2025:
                print("Năm sản xuất không hợp lệ! Vui lòng nhập lại.")
                continue
            vehicles = self.controller.search_by_year(year)
            if vehicles is not None:
                return

    # 8. Đếm số lượng xe
    def dem_so_luong_xe(self):
        self.controller.count_all()

    # 9. Xe mới nhất
    def xe_moi_nhat(self):
        self.controller.get_latest_vehicle()

    # 10. Phân trang
    def ds_xe_phan_trang(self):
        offset = self.get_input("Nhập offset (bỏ qua bao nhiêu xe, nhập 0 để hủy): ", cast_func=int)
        if offset is None:
            return
        limit = self.get_input("Nhập số xe muốn hiển thị (nhập 0 để hủy): ", cast_func=int)
        if limit is None:
            return
        self.controller.list_vehicles_paged(offset, limit)
