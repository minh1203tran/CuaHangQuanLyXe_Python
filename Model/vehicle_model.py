from MSSQLServer.MSSQLServer import Database

class VehicleModel:
    def __init__(self):
        self.conn = Database.get_instance()

    # 1. Danh sách tất cả xe
    def get_all(self):
        sql = "SELECT * FROM VEHICLES"
        return self.conn.query(sql)

    # 2. Thêm xe
    def add_vehicle(self, license_plate, model, manufacturer, year, price):
        sql = "INSERT INTO VEHICLES (LICENSEPLATE, MODEL, MANUFACTURER, YEAR, PRICE) VALUES (?, ?, ?, ?, ?)"
        return self.conn.query(sql, (license_plate, model, manufacturer, year, price))

    # Kiểm tra biển số đã tồn tại trong database chưa
    def check_license_plate_exists(self, license_plate: str) -> bool:
        sql = "SELECT COUNT(*) FROM VEHICLES WHERE UPPER(LICENSEPLATE) = UPPER(?)"
        result = self.conn.query(sql, (license_plate,))
        return result[0][0] > 0 if result else False

    # 3. Cập nhật thông tin xe
    def update_vehicle(self, vehicle_id, license_plate, model, manufacturer, year, price):
        sql = """UPDATE VEHICLES 
                 SET LICENSEPLATE = ?, MODEL = ?, MANUFACTURER = ?, YEAR = ?, PRICE = ?
                 WHERE VEHICLESID = ?"""
        return self.conn.query(sql, (license_plate, model, manufacturer, year, price, vehicle_id))

    # 4. Xóa xe
    def delete_vehicle(self, vehicle_id):
        sql = "DELETE FROM VEHICLES WHERE VEHICLESID = ?"
        return self.conn.query(sql, (vehicle_id,))

    def has_orders(self, vehicle_id):
        sql = "SELECT COUNT(*) FROM ORDERDETAILS WHERE VEHICLESID = ?"
        try:
            result = self.conn.query(sql, (vehicle_id,))
            if not result:
                return False
            return result[0][0] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra đơn hàng: {e}")
            return False

    # 5. Lấy thông tin xe theo ID
    def get_vehicle_by_id(self, vehicle_id):
        sql = "SELECT * FROM VEHICLES WHERE VEHICLESID = ?"
        result = self.conn.query(sql, (vehicle_id,))
        if result and len(result) > 0:
            return result[0]
        else:
            return None

    # 6. Tìm kiếm theo hãng
    def search_by_manufacturer(self, manufacturer):
        sql = "SELECT * FROM VEHICLES WHERE MANUFACTURER LIKE ?"
        return self.conn.query(sql, ('%' + manufacturer + '%',))

    # 7. Tìm kiếm theo năm sản xuất
    def search_by_year(self, year):
        sql = "SELECT * FROM VEHICLES WHERE YEAR = ?"
        return self.conn.query(sql, (year,))

    # 8. Đếm số lượng xe
    def count_all(self):
        sql = "SELECT COUNT(*) FROM VEHICLES"
        return self.conn.query(sql)

    # 9. Xe mới nhất
    def get_latest_vehicle(self):
        sql = "SELECT TOP 1 * FROM VEHICLES ORDER BY YEAR DESC"
        return self.conn.query(sql)

    # 10. Phân trang
    def get_paged(self, offset, limit):
        sql = """SELECT * FROM VEHICLES
                 ORDER BY VEHICLESID
                 OFFSET ? ROWS
                 FETCH NEXT ? ROWS ONLY"""
        return self.conn.query(sql, (offset, limit))
