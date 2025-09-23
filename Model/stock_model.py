from MSSQLServer.MSSQLServer import Database

class StockModel:
    def __init__(self):
        self.db = Database.get_instance()

    # 1. Xem danh sách tồn kho
    def get_all(self):
        sql = """
        SELECT S.STOCKID, S.VEHICLESID, V.MODEL, V.MANUFACTURER, 
               S.QUANTITYAVAILABLE, S.MINSTOCKLEVEL, S.LASTRESTOCKDATE
        FROM STOCKS S
        JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        """
        return self.db.query(sql)

    # 2. Thêm tồn kho mới
    def insert(self, vehicle_id, qty, min_level):
        sql = """
        INSERT INTO STOCKS (VEHICLESID, QUANTITYAVAILABLE, MINSTOCKLEVEL, LASTRESTOCKDATE)
        VALUES (?, ?, ?, GETDATE())
        """
        return self.db.query(sql, (vehicle_id, qty, min_level))

    def exists(self, vehicle_id):
        sql = "SELECT 1 FROM STOCKS WHERE VEHICLESID = ?"
        result = self.db.query(sql, (vehicle_id,))
        return result and len(result) > 0

    # 3. Cập nhật tồn kho
    def update(self, stock_id, qty, min_level):
        sql = """
        UPDATE STOCKS 
        SET QUANTITYAVAILABLE = ?, MINSTOCKLEVEL = ?, LASTRESTOCKDATE = GETDATE()
        WHERE STOCKID = ?
        """
        rowcount = self.db.query(sql, (qty, min_level, stock_id))
        if rowcount is None:
            return False
        return rowcount > 0

    # 4. Xóa tồn kho
    def delete(self, stock_id):
        sql = "DELETE FROM STOCKS WHERE STOCKID = ?"
        return self.db.query(sql, (stock_id,))

    # 5. Tìm kiếm tồn kho theo xe
    def search_by_vehicle(self, keyword):
        sql = """
        SELECT S.STOCKID, S.VEHICLESID, V.LICENSEPLATE, V.MODEL, V.MANUFACTURER, 
               S.QUANTITYAVAILABLE, S.MINSTOCKLEVEL, S.LASTRESTOCKDATE
        FROM STOCKS S
        JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        WHERE V.MODEL LIKE ? OR V.MANUFACTURER LIKE ?
        """
        like_kw = f"%{keyword}%"
        return self.db.query(sql, (like_kw, like_kw))

    # 6. Báo cáo tồn dưới mức tối thiểu
    def report_below_min(self):
        sql = """
        SELECT S.STOCKID, V.MODEL, V.MANUFACTURER, S.QUANTITYAVAILABLE, S.MINSTOCKLEVEL
        FROM STOCKS S
        JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        WHERE S.QUANTITYAVAILABLE < S.MINSTOCKLEVEL
        """
        return self.db.query(sql)

    # 7. Báo cáo xe âm
    def report_negative_stock(self):
        sql = """
        SELECT S.STOCKID, V.MODEL, V.MANUFACTURER, S.QUANTITYAVAILABLE
        FROM STOCKS S
        JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        WHERE S.QUANTITYAVAILABLE < 0
        """
        return self.db.query(sql)

    # 8. Xuất kho nhanh
    def stock_out(self, stock_id, qty):
        sql = """
        UPDATE STOCKS
        SET QUANTITYAVAILABLE = QUANTITYAVAILABLE - ?, LASTRESTOCKDATE = GETDATE()
        WHERE STOCKID = ?
        """
        return self.db.query(sql, (qty, stock_id))