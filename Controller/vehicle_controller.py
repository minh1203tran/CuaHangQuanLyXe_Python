from model.vehicle_model import VehicleModel
from view.vehicle_view import VehicleView

class VehicleController:
    def __init__(self):
        self.model = VehicleModel()
        self.view = VehicleView()

    # 1. Danh sách tất cả xe
    def list_vehicles(self):
        data = self.model.get_all()
        self.view.show_list(data)

    # 2. Thêm xe
    def add_vehicle(self, license_plate, model, manufacturer, year, price):
        if self.check_license_plate_exists(license_plate):
            self.view.show_error("Biển số đã tồn tại trong hệ thống!")
            return False

        result = self.model.add_vehicle(license_plate, model, manufacturer, year, price)
        if result:
            self.view.show_message("Đã thêm xe thành công!")
            return True
        else:
            self.view.show_message("Thêm xe thất bại!")
            return False

    def check_license_plate_exists(self, license_plate: str) -> bool:
        return self.model.check_license_plate_exists(license_plate)

    # 3. Cập nhật thông tin xe
    def update_vehicle(self, vehicle_id, license_plate, model, manufacturer, year, price):
        result = self.model.update_vehicle(vehicle_id, license_plate, model, manufacturer, year, price)
        if result:
            self.view.show_message("Cập nhật thành công!")
        else:
            self.view.show_message("Cập nhật thất bại!")

    # 4. Xóa xe
    def delete_vehicle(self, vehicle_id):
        if self.model.has_orders(vehicle_id):
            self.view.show_message("Xe đang có đơn hàng, không thể xóa!")
            return
        result = self.model.delete_vehicle(vehicle_id)
        if result and result > 0:
            self.view.show_message("Đã xóa xe!")
        else:
            self.view.show_message("Không tìm thấy xe để xóa!")

    # 5. Lấy thông tin xe theo ID
    def get_vehicle_by_id(self, vehicle_id):
        data = self.model.get_vehicle_by_id(vehicle_id)
        if data:
            self.view.show_detail(data)
            return data
        else:
            self.view.show_message("Không tìm thấy xe!")
            return None

    # 6. Tìm kiếm theo hãng
    def search_by_manufacturer(self, manufacturer):
        return self.model.search_by_manufacturer(manufacturer)

    # 7. Tìm kiếm theo năm sản xuất
    def search_by_year(self, year):
        data = self.model.search_by_year(year)
        if data and len(data) > 0:
            self.view.show_list(data)
            return data
        else:
            self.view.show_message(f"Không tìm thấy xe nào sản xuất năm {year}!")
            return None

    # 8. Đếm số lượng xe
    def count_all(self):
        data = self.model.count_all()
        self.view.show_message(f"Tổng số xe: {data[0][0]}")

    # 9. Xe mới nhất
    def get_latest_vehicle(self):
        data = self.model.get_latest_vehicle()
        self.view.show_list(data)

    # 10. Phân trang
    def list_vehicles_paged(self, offset, limit):
        data = self.model.get_paged(offset, limit)
        self.view.show_list(data)