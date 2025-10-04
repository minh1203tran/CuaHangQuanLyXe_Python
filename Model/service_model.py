from MSSQLServer.MSSQLServer import Database

class ServiceModel:
    def __init__(self):
        self.db = Database.get_instance()

    def get_customers_for_selection(self, keyword=None):
        if keyword:
            sql = "SELECT CUSTOMERID, FULLNAME, PHONE FROM CUSTOMERS WHERE FULLNAME LIKE ? OR PHONE LIKE ?"
            return self.db.query(sql, (f"%{keyword}%", f"%{keyword}%"))
        else:
            sql = "SELECT CUSTOMERID, FULLNAME, PHONE FROM CUSTOMERS"
            return self.db.query(sql)

    # 1. Danh sách dịch vụ
    def get_all(self):
        sql = """
        SELECT S.SERVICEID, S.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME,
               S.VEHICLESID, V.MODEL AS VEHICLEMODEL,
               S.SERVICETYPE, S.SERVICEDATE, S.COST,
               S.TECHNICIANID, U.FULLNAME AS TECHNICIANNAME,
               S.STATUS
        FROM SERVICES S
        LEFT JOIN CUSTOMERS C ON S.CUSTOMERID = C.CUSTOMERID
        LEFT JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        LEFT JOIN USERS U ON S.TECHNICIANID = U.USERID
        ORDER BY S.SERVICEDATE DESC
        """
        return self.db.query(sql)

    # 2. Thêm dịch vụ mới
    def insert(self, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status):
        sql = """
        INSERT INTO SERVICES (CUSTOMERID, VEHICLESID, SERVICETYPE, SERVICEDATE, COST, TECHNICIANID, STATUS)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.query(sql, (customer_id, vehicle_id, service_type, service_date, cost, technician_id, status))

    def get_vehicles_for_selection(self, keyword=None):
        if keyword:
            sql = "SELECT VEHICLESID, MODEL, MANUFACTURER, YEAR FROM VEHICLES WHERE MANUFACTURER LIKE ?"
            return self.db.query(sql, (f"%{keyword}%",))
        else:
            sql = "SELECT VEHICLESID, MODEL, MANUFACTURER, YEAR FROM VEHICLES"
            return self.db.query(sql)

    def get_technicians_for_selection(self, keyword=None):
        if keyword:
            sql = "SELECT USERID, FULLNAME FROM USERS WHERE FULLNAME LIKE ? AND ROLE = 'STAFF'"
            return self.db.query(sql, (f"%{keyword}%",))
        else:
            sql = "SELECT USERID, FULLNAME FROM USERS WHERE ROLE = 'STAFF'"
            return self.db.query(sql)

    # 3. Cập nhật dịch vụ
    def update(self, service_id, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status):
        sql = """
        UPDATE SERVICES
        SET CUSTOMERID = ?, VEHICLESID = ?, SERVICETYPE = ?, SERVICEDATE = ?, COST = ?, TECHNICIANID = ?, STATUS = ?
        WHERE SERVICEID = ?
        """
        return self.db.query(sql,
            (customer_id, vehicle_id, service_type, service_date, cost, technician_id, status, service_id))

    def get_by_id(self, service_id):
        sql = """
        SELECT S.SERVICEID, S.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME, C.PHONE AS CUSTOMERPHONE,
               S.VEHICLESID, V.MANUFACTURER AS VEHICLEMANUFACTURER,
               S.SERVICETYPE, S.SERVICEDATE, S.COST,
               S.TECHNICIANID, U.FULLNAME AS TECHNICIANNAME,
               S.STATUS
        FROM SERVICES S
        LEFT JOIN CUSTOMERS C ON S.CUSTOMERID = C.CUSTOMERID
        LEFT JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        LEFT JOIN USERS U ON S.TECHNICIANID = U.USERID
        WHERE S.SERVICEID = ?
        """
        rows = self.db.query(sql, (service_id,))
        return rows[0] if rows else None

    # 4. Xóa dịch vụ
    def delete(self, service_id):
        sql = "DELETE FROM SERVICES WHERE SERVICEID = ?"
        return self.db.query(sql, (service_id,))

    # 5. Tìm kiếm dịch vụ
    def search(self, keyword):
        sql = """
        SELECT S.SERVICEID, S.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME,
               S.VEHICLESID, V.MODEL AS VEHICLEMODEL,
               S.SERVICETYPE, S.SERVICEDATE, S.COST,
               S.TECHNICIANID, U.FULLNAME AS TECHNICIANNAME,
               S.STATUS
        FROM SERVICES S
        LEFT JOIN CUSTOMERS C ON S.CUSTOMERID = C.CUSTOMERID
        LEFT JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        LEFT JOIN USERS U ON S.TECHNICIANID = U.USERID
        WHERE C.FULLNAME LIKE ? OR V.MODEL LIKE ? OR U.FULLNAME LIKE ? OR S.SERVICETYPE LIKE ?
        ORDER BY S.SERVICEDATE DESC
        """
        return self.db.query(sql, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    # 7. Lọc theo trạng thái
    def filter_by_status(self, status):
        sql = """
        SELECT S.SERVICEID, S.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME,
               S.VEHICLESID, V.MODEL AS VEHICLEMODEL,
               S.SERVICETYPE, S.SERVICEDATE, S.COST,
               S.TECHNICIANID, U.FULLNAME AS TECHNICIANNAME,
               S.STATUS
        FROM SERVICES S
        LEFT JOIN CUSTOMERS C ON S.CUSTOMERID = C.CUSTOMERID
        LEFT JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        LEFT JOIN USERS U ON S.TECHNICIANID = U.USERID
        WHERE S.STATUS = ?
        ORDER BY S.SERVICEDATE DESC
        """
        return self.db.query(sql, (status,))

    # 8. Lọc theo ngày
    def filter_by_date(self, start_date, end_date):
        sql = """
        SELECT S.SERVICEID, S.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME,
               S.VEHICLESID, V.MODEL AS VEHICLEMODEL,
               S.SERVICETYPE, S.SERVICEDATE, S.COST,
               S.TECHNICIANID, U.FULLNAME AS TECHNICIANNAME,
               S.STATUS
        FROM SERVICES S
        LEFT JOIN CUSTOMERS C ON S.CUSTOMERID = C.CUSTOMERID
        LEFT JOIN VEHICLES V ON S.VEHICLESID = V.VEHICLESID
        LEFT JOIN USERS U ON S.TECHNICIANID = U.USERID
        WHERE S.SERVICEDATE BETWEEN ? AND ?
        ORDER BY S.SERVICEDATE DESC
        """
        return self.db.query(sql, (start_date, end_date))

    # 9. Thống kê dịch vụ
    def get_service_stats_by_status(self):
        sql = """
        SELECT STATUS, COUNT(*) AS count
        FROM SERVICES
        GROUP BY STATUS
        """
        return self.db.query(sql)

    def get_service_stats_by_type(self):
        sql = """
        SELECT SERVICETYPE, SUM(COST) AS total_cost
        FROM SERVICES
        GROUP BY SERVICETYPE
        ORDER BY total_cost DESC
        """
        return self.db.query(sql)