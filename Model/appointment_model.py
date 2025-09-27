from MSSQLServer.MSSQLServer import Database
# from datetime import datetime, date, time

class AppointmentModel:
    def __init__(self):
        self.db = Database.get_instance()

    def get_customers_for_selection(self, keyword=None):
        if keyword:
            sql = "SELECT CUSTOMERID, FULLNAME, PHONE FROM CUSTOMERS WHERE FULLNAME LIKE ? OR PHONE LIKE ?"
            return self.db.query(sql, (f"%{keyword}%", f"%{keyword}%"))
        else:
            sql = "SELECT CUSTOMERID, FULLNAME, PHONE FROM CUSTOMERS"
            return self.db.query(sql)

    # 1. Danh sách lịch hẹn
    def get_all(self):
        sql = """
        SELECT A.APPOINTMENTID, A.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME, C.PHONE AS CUSTOMERPHONE,
               A.PURPOSE, A.APPOINTMENTDATE, A.STATUS
        FROM APPOINTMENTS A
        JOIN CUSTOMERS C ON A.CUSTOMERID = C.CUSTOMERID
        ORDER BY A.APPOINTMENTDATE DESC
        """
        return self.db.query(sql)

    # 2. Thêm lịch hẹn mới
    def insert(self, customer_id, purpose, appointment_datetime, status):
        sql = """
        INSERT INTO APPOINTMENTS (CUSTOMERID, PURPOSE, APPOINTMENTDATE, STATUS)
        VALUES (?, ?, ?, ?)
        """
        return self.db.query(sql, (customer_id, purpose, appointment_datetime, status))

    # 3. Cập nhật lịch hẹn
    def update(self, appointment_id, customer_id, purpose, appointment_date, status):
        sql = """
        UPDATE APPOINTMENTS
        SET CUSTOMERID = ?, PURPOSE = ?, APPOINTMENTDATE = ?, STATUS = ?
        WHERE APPOINTMENTID = ?
        """
        return self.db.query(sql,
            (customer_id, purpose, appointment_date, status, appointment_id))

    def get_by_id(self, appointment_id):
        sql = """
        SELECT A.APPOINTMENTID, A.CUSTOMERID, C.FULLNAME AS CUSTOMERNAME, C.PHONE AS CUSTOMERPHONE,
               A.PURPOSE, A.APPOINTMENTDATE, A.STATUS
        FROM APPOINTMENTS A
        JOIN CUSTOMERS C ON A.CUSTOMERID = C.CUSTOMERID
        WHERE A.APPOINTMENTID = ?
        """
        rows = self.db.query(sql, (appointment_id,))
        return rows[0] if rows else None

    # 4. Xóa lịch hẹn
    def delete(self, appointment_id):
        sql = "DELETE FROM APPOINTMENTS WHERE APPOINTMENTID = ?"
        return self.db.query(sql, (appointment_id,))

    # 5. Tìm kiếm lịch hẹn
    def search(self, keyword):
        sql = """
        SELECT A.APPOINTMENTID, A.CUSTOMERID, C.FULLNAME AS CUSTOMER_NAME, C.PHONE AS CUSTOMER_PHONE,
               A.PURPOSE, A.APPOINTMENTDATE, A.STATUS
        FROM APPOINTMENTS A
        JOIN CUSTOMERS C ON A.CUSTOMERID = C.CUSTOMERID
        WHERE C.FULLNAME LIKE ? OR C.PHONE LIKE ?
        ORDER BY A.APPOINTMENTDATE DESC
        """
        return self.db.query(sql, (f"%{keyword}%", f"%{keyword}%"))

    # 7. Lọc theo trạng thái
    def filter_by_status(self, status):
        sql = """
        SELECT A.APPOINTMENTID, A.CUSTOMERID, C.FULLNAME AS CUSTOMER_NAME, C.PHONE AS CUSTOMER_PHONE,
               A.PURPOSE, A.APPOINTMENTDATE, A.STATUS
        FROM APPOINTMENTS A
        JOIN CUSTOMERS C ON A.CUSTOMERID = C.CUSTOMERID
        WHERE A.STATUS = ?
        ORDER BY A.APPOINTMENTDATE DESC
        """
        return self.db.query(sql, (status,))

    # 8. Lọc theo ngày
    def filter_by_date(self, start_date, end_date):
        sql = """
        SELECT A.APPOINTMENTID, A.CUSTOMERID, C.FULLNAME AS CUSTOMER_NAME, C.PHONE AS CUSTOMER_PHONE,
               A.PURPOSE, A.APPOINTMENTDATE, A.STATUS
        FROM APPOINTMENTS A
        JOIN CUSTOMERS C ON A.CUSTOMERID = C.CUSTOMERID
        WHERE A.APPOINTMENTDATE BETWEEN ? AND ?
        ORDER BY A.APPOINTMENTDATE DESC
        """
        return self.db.query(sql, (start_date, end_date))

    # 9. Thống kê lịch hẹn
    def stats_by_status(self):
        sql = """
        SELECT STATUS, COUNT(*) AS count
        FROM APPOINTMENTS
        GROUP BY STATUS
        """
        return self.db.query(sql)