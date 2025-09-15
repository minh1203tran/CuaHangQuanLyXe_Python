import re
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
            lp = self.get_input("Biển số: ", cast_func=str)
            if lp is None:
                return
            lp = lp.upper()
            if not self.validate_license_plate(lp):
                print("Biển số không hợp lệ! Vui lòng nhập lại.")
                continue
            if self.controller.check_license_plate_exists(lp):
                print("Biển số đã tồn tại trong hệ thống! Vui lòng nhập lại.")
                continue
            break
        model = self.get_input("Mẫu xe: ", cast_func=str)
        if model is None:
            return
        manu = self.get_input("Hãng: ", cast_func=str)
        if manu is None:
            return
        while True:
            year = self.get_input("Năm SX: ", cast_func=int)
            if year is None:
                return
            if year > 2025:
                print("Năm sản xuất phải bé hơn hoặc bằng năm hiện tại!")
                continue
            break
        self.controller.add_vehicle(lp, model, manu, year)

    # 3. Cập nhật thông tin xe
    def cap_nhat_xe(self):
        vid = self.get_input("Nhập ID xe cần cập nhật (0 để hủy): ", cast_func=int)
        if vid is None:
            return
        current_vehicle = self.controller.get_vehicle_by_id(vid)
        if not current_vehicle:
            print("Không tìm thấy xe với ID này!")
            return
        print("\n--- Nhập thông tin mới (Enter để giữ nguyên, 0 để hủy) ---")
        lp = self.get_input("Biển số mới: ", default=current_vehicle[1], to_upper=True,
                       validator=self.validate_license_plate)
        if lp is None:
            return
        model = self.get_input("Mẫu xe mới: ", default=current_vehicle[2])
        if model is None:
            return
        manu = self.get_input("Hãng mới: ", default=current_vehicle[3])
        if manu is None:
            return
        year = self.get_input("Năm SX mới: ", default=current_vehicle[4], cast_func=int,
                         validator=lambda y: y <= 2025)
        if year is None:
            return
        confirm = input("Bạn có chắc chắn muốn cập nhật xe này? (Y/N): ").strip().upper()
        if confirm == "Y":
            self.controller.update_vehicle(vid, lp, model, manu, year)
        else:
            print("Hủy cập nhật xe.")
        self.controller.update_vehicle(vid, lp, model, manu, year)

    # 4. Xóa xe
    def xoa_xe(self):
        vid = self.get_input("Nhập ID xe cần xóa (0 để hủy): ", cast_func=int)
        if vid is None:
            return
        confirm = input(f"Bạn có chắc chắn muốn xóa xe với ID {vid}? (Y/N): ").strip().upper()
        if confirm == "Y":
            self.controller.delete_vehicle(vid)
        else:
            print("Hủy thao tác xóa, quay lại menu chính!")

    # 5. Lấy thông tin xe theo ID
    def xem_chi_tiet_xe(self):
        vid = self.get_input("Nhập ID xe (0 để hủy): ", cast_func=int)
        if vid is None:
            return
        self.controller.get_vehicle_by_id(vid)

    # 6. Tìm kiếm theo hãng
    def tim_theo_hang(self):
        manu = self.get_input("Nhập tên hãng (0 để hủy): ", cast_func=str)
        if manu is None:
            return
        self.controller.search_by_manufacturer(manu)

    # 7. Tìm kiếm theo năm sản xuất
    def tim_theo_nam(self):
        year = self.get_input("Nhập năm sản xuất (0 để hủy): ", cast_func=int)
        if year is None:
            return
        self.controller.search_by_year(year)

    # 8. Đếm số lượng xe
    def dem_so_luong_xe(self):
        choice = self.get_input("Nhấn Enter để tiếp tục, hoặc 0 để hủy: ", cast_func=str)
        if choice is None:
            return
        self.controller.count_all()

    # 9. Xe mới nhất
    def xe_moi_nhat(self):
        choice = self.get_input("Nhấn Enter để xem xe mới nhất, hoặc 0 để hủy: ", cast_func=str)
        if choice is None:
            return
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
