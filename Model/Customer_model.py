from MSSQLServer.MSSQLServer import Database

class CustomerModel:
    def __init__(self):
        self.conn = Database.get_instance()

    # 1. Xem danh sách khách hàng
    def get_all_customers(self):
        sql = "SELECT CUSTOMERID, USERNAME, FULLNAME, EMAIL, PHONE, ADDRESS, ID_CARD, CREATED_AT, STATUS FROM CUSTOMERS"
        return self.conn.query(sql)

    # 2. Thêm khách hàng mới
    def add_customer(self, username, fullname, email, phone, address, id_card):
        sql = """
        INSERT INTO CUSTOMERS (USERNAME, FULLNAME, EMAIL, PHONE, ADDRESS, ID_CARD)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.conn.query(sql, (username, fullname, email, phone, address, id_card))

    def check_username_exists(self, username):
        sql = "SELECT COUNT(*) FROM CUSTOMERS WHERE USERNAME = ?"
        result = self.conn.query(sql, (username,))
        return result[0][0] > 0 if result else False

    def check_email_exists(self, email):
        sql = "SELECT COUNT(*) FROM CUSTOMERS WHERE EMAIL = ?"
        result = self.conn.query(sql, (email,))
        result = self.conn.query(sql, (email,))
        return result[0][0] > 0 if result else False

    def check_phone_exists(self, phone):
        sql = "SELECT 1 FROM CUSTOMERS WHERE PHONE = ?"
        rows = self.conn.query(sql, (phone,))
        return len(rows) > 0

    # 3. Cập nhật khách hàng
    def update_customer(self, cid, fullname, email, phone, address, id_card):
        sql = """UPDATE CUSTOMERS SET FULLNAME = ?, EMAIL = ?, PHONE = ?, ADDRESS = ?, ID_CARD = ? WHERE CUSTOMERID = ?"""
        cursor = self.conn.cursor()
        cursor.execute(sql, (fullname, email, phone, address, id_card, cid))
        self.conn.commit()
        return cursor.rowcount

    # 4. Xóa khách hàng
    def delete_customer(self, cid):
        try:
            sql = "DELETE FROM CUSTOMERS WHERE CUSTOMERID=?"
            cursor = self.conn.cursor()
            cursor.execute(sql, (cid,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            err = str(e)
            if "REFERENCE constraint" in err:
                return "constraint"
            return "error"

    # 5. Xem chi tiết khách hàng theo ID
    def get_customer_by_id(self, cid):
        sql = "SELECT CUSTOMERID, USERNAME, FULLNAME, EMAIL, PHONE, ADDRESS, ID_CARD, CREATED_AT, STATUS FROM CUSTOMERS WHERE CUSTOMERID=?"
        rows = self.conn.query(sql, (cid,))
        return rows[0] if rows else None

    # 6. Khóa/Mở khóa khách hàng
    def set_status(self, cid, status):
        sql = "UPDATE CUSTOMERS SET STATUS = ? WHERE CUSTOMERID = ?"
        return self.conn.query(sql, (status, cid))

    # 7. Tìm khách hàng theo tên/SĐT/Email
    def search_customer(self, keyword):
        sql = """
            SELECT CUSTOMERID, USERNAME, FULLNAME, EMAIL, PHONE, ADDRESS, ID_CARD, CREATED_AT, STATUS
            FROM CUSTOMERS
            WHERE USERNAME LIKE ? OR FULLNAME LIKE ? OR EMAIL LIKE ? OR PHONE LIKE ?
        """
        return self.conn.query(sql, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    # 8. Thống kê
    def count_customers(self):
        sql = "SELECT COUNT(*) FROM CUSTOMERS"
        result = self.conn.query(sql)
        return result[0][0] if result else 0

    def count_by_status(self, status):
        sql = "SELECT COUNT(*) FROM CUSTOMERS WHERE STATUS = ?"
        result = self.conn.query(sql, (status,))
        return result[0][0] if result else 0

    # 9. Khách hàng mới nhất
    def latest_customer(self):
        sql = """
           SELECT TOP 1 CUSTOMERID, USERNAME, FULLNAME, EMAIL, PHONE, ADDRESS, ID_CARD, CREATED_AT, STATUS
           FROM CUSTOMERS
           ORDER BY CREATED_AT DESC
           """
        result = self.conn.query(sql)
        if result and len(result) > 0:
            return result[0]
        return None