from MSSQLServer.MSSQLServer import Database

class PaymentModel:
    def __init__(self):
        self.db = Database.get_instance()

    # 1. Danh sách thanh toán
    def get_all(self):
        sql = "SELECT * FROM PAYMENTS ORDER BY PAYMENTDATE DESC"
        return self.db.query(sql)

    # 2. Thêm thanh toán
    def insert(self, order_id, amount, method, transaction_id, status):
        sql = """
        INSERT INTO PAYMENTS (ORDERID, AMOUNT, PAYMENTDATE, PAYMENTMETHOD, TRANSACTIONID, STATUS)
        VALUES (?, ?, GETDATE(), ?, ?, ?)
        """
        return self.db.query(sql, (order_id, amount, method, transaction_id, status))

    def has_payment(self, order_id):
        sql = """
            SELECT 1 
            FROM PAYMENTS 
            WHERE ORDERID = ?
        """
        result = self.db.query(sql, (order_id,))
        return bool(result)

    # 3. Cập nhật thanh toán
    def update(self, payment_id, amount, method, status):
        sql = """
        UPDATE PAYMENTS
        SET AMOUNT = ?, PAYMENTMETHOD = ?, STATUS = ?
        WHERE PAYMENTID = ?
        """
        return self.db.query(sql, (amount, method, status, payment_id))

    def get_order_total(self, order_id):
        sql = "SELECT TOTALAMOUNT FROM ORDERS WHERE ORDERID = ?"
        result = self.db.query(sql, (order_id,))
        return result[0] if result else None

    def get_payments_by_order(self, order_id):
        sql = "SELECT PAYMENTID, AMOUNT FROM PAYMENTS WHERE ORDERID = ?"
        return self.db.query(sql, (order_id,))

    def get_by_id(self, payment_id):
        sql = """
        SELECT P.PAYMENTID, P.ORDERID, C.FULLNAME, C.PHONE,
               P.AMOUNT, P.PAYMENTMETHOD, P.TRANSACTIONID, 
               P.STATUS, P.PAYMENTDATE
        FROM PAYMENTS P
        JOIN ORDERS O ON P.ORDERID = O.ORDERID
        JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
        WHERE P.PAYMENTID = ?
        """
        rows = self.db.query(sql, (payment_id,))
        return rows[0] if rows else None

    # 4. Xóa thanh toán
    def delete(self, payment_id):
        sql = "DELETE FROM PAYMENTS WHERE PAYMENTID = ?"
        return self.db.query(sql, (payment_id,))

    # 5. Tìm kiếm thanh toán
    def search(self, keyword):
        sql = """
        SELECT P.PAYMENTID, P.ORDERID, C.FULLNAME, C.PHONE, P.AMOUNT, P.PAYMENTMETHOD, P.TRANSACTIONID, 
               P.STATUS, P.PAYMENTDATE
        FROM PAYMENTS P
        JOIN ORDERS O ON P.ORDERID = O.ORDERID
        JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
        WHERE C.FULLNAME LIKE ? OR C.PHONE LIKE ?
        ORDER BY P.PAYMENTDATE DESC
        """
        return self.db.query(sql, (f"%{keyword}%", f"%{keyword}%"))

    # 7. Lọc theo trạng thái
    def filter_by_status(self, status):
        sql = "SELECT * FROM PAYMENTS WHERE STATUS=? ORDER BY PAYMENTDATE DESC"
        return self.db.query(sql, (status,))

    # 8. Thống kê thanh toán
    def stats_total_amount(self):
        sql = """
        SELECT STATUS, COUNT(*) AS count, SUM(AMOUNT) AS total
        FROM PAYMENTS
        GROUP BY STATUS
        """
        return self.db.query(sql)  # dùng query thay vì cursor.execute
