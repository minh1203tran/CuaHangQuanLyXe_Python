from MSSQLServer.MSSQLServer import Database

class OrderModel:
    def __init__(self):
        self.conn = Database.get_instance()

    # 1. Xem danh sách đơn hàng
    def get_all_orders(self):
        sql = """
            SELECT O.ORDERID, O.CUSTOMERID, C.FULLNAME, O.USERID, U.USERNAME,
                   O.ORDERDATE, O.TOTALAMOUNT, O.STATUS, O.PAYMENTMETHOD,
                   O.DELIVERYADDRESS, O.NOTE
            FROM ORDERS O
            JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
            JOIN USERS U ON O.USERID = U.USERID
        """
        return self.conn.query(sql)

    # 2. Xem chi tiết đơn hàng
    def get_order_by_id(self, order_id):
        sql = """
            SELECT O.ORDERID, O.CUSTOMERID, C.FULLNAME, O.USERID, U.USERNAME,
                   O.ORDERDATE, O.TOTALAMOUNT, O.STATUS, O.PAYMENTMETHOD,
                   O.DELIVERYADDRESS, O.NOTE
            FROM ORDERS O
            JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
            JOIN USERS U ON O.USERID = U.USERID
            WHERE O.ORDERID = ?
        """
        rows = self.conn.query(sql, (order_id,))
        return rows[0] if rows else None

    def get_order_details(self, order_id):
        sql = """
            SELECT OD.ORDERDETAILID, OD.VEHICLESID, V.MODEL, OD.QUANTITY, OD.UNITPRICE, OD.SUBTOTAL
            FROM ORDERDETAILS OD
            JOIN VEHICLES V ON OD.VEHICLESID = V.VEHICLESID
            WHERE OD.ORDERID=?
        """
        return self.conn.query(sql, (order_id,))

    # 3. Tạo đơn hàng mới
    def add_order(self, customer_id, user_id, payment_method, delivery_address, note):
        sql = """
            INSERT INTO ORDERS (CUSTOMERID, USERID, PAYMENTMETHOD, DELIVERYADDRESS, NOTE, TOTALAMOUNT)
            VALUES (?, ?, ?, ?, ?, 0)
        """
        return self.conn.query(sql, (customer_id, user_id, payment_method, delivery_address, note))

    def latest_order(self):
        sql = "SELECT TOP 1 * FROM ORDERS ORDER BY ORDERDATE DESC"
        rows = self.conn.query(sql)
        return rows[0] if rows else None

    def add_order_detail(self, order_id, vehicle_id, quantity, unit_price):
        sql = """
            INSERT INTO ORDERDETAILS (ORDERID, VEHICLESID, QUANTITY, UNITPRICE)
            VALUES (?, ?, ?, ?)
        """
        self.conn.query(sql, (order_id, vehicle_id, quantity, unit_price))
        sql_total = "SELECT SUM(SUBTOTAL) FROM ORDERDETAILS WHERE ORDERID=?"
        total = self.conn.query(sql_total, (order_id,))[0][0] or 0
        self.update_order_total(order_id, total)

    def update_order_total(self, order_id, total_amount):
        sql = "UPDATE ORDERS SET TOTALAMOUNT=? WHERE ORDERID=?"
        return self.conn.query(sql, (total_amount, order_id))

    # 4. Cập nhật trạng thái đơn hàng
    def update_order_status(self, order_id, new_status):
        sql_get = "SELECT STATUS FROM ORDERS WHERE ORDERID=?"
        rows = self.conn.query(sql_get, (order_id,))
        old_status = rows[0][0] if rows else None
        sql_update = "UPDATE ORDERS SET STATUS=? WHERE ORDERID=?"
        self.conn.query(sql_update, (new_status, order_id))
        return old_status, new_status

    # 5. Tìm kiếm đơn hàng
    def search_orders(self, keyword=None, limit=20):
        if not keyword:
            return []
        sql = f"""
            SELECT TOP {limit} O.ORDERID, C.FULLNAME, C.PHONE, O.STATUS, O.ORDERDATE
            FROM ORDERS O
            JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
            WHERE C.FULLNAME LIKE ? OR CAST(C.PHONE AS VARCHAR) LIKE ?
            ORDER BY O.ORDERDATE DESC
        """
        pattern = f"%{keyword}%"
        return self.conn.query(sql, (pattern, pattern))

    # 6. Thống kê đơn hàng
    def get_orders_by_status(self, status):
        sql = """
            SELECT O.ORDERID, C.FULLNAME, C.PHONE, O.TOTALAMOUNT, O.STATUS, O.ORDERDATE
            FROM ORDERS O
            JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
            WHERE O.STATUS = ?
            ORDER BY O.ORDERDATE DESC
        """
        return self.conn.query(sql, (status,))

    def get_sales_statistics(self, period='month'):
        if period == 'month':
            sql = """
                SELECT 
                    YEAR(ORDERDATE) as Year,
                    MONTH(ORDERDATE) as Month,
                    COUNT(*) as OrderCount,
                    SUM(TOTALAMOUNT) as TotalRevenue
                FROM ORDERS
                WHERE STATUS != 'Đã hủy'
                GROUP BY YEAR(ORDERDATE), MONTH(ORDERDATE)
                ORDER BY Year DESC, Month DESC
            """
        else:
            sql = """
                SELECT 
                    CONVERT(DATE, ORDERDATE) as OrderDate,
                    COUNT(*) as OrderCount,
                    SUM(TOTALAMOUNT) as TotalRevenue
                FROM ORDERS
                WHERE STATUS != 'Đã hủy'
                GROUP BY CONVERT(DATE, ORDERDATE)
                ORDER BY OrderDate DESC
            """
        return self.conn.query(sql)

    def get_orders_by_date_range(self, start_date, end_date):
        sql = """
            SELECT O.ORDERID, C.FULLNAME, C.PHONE, O.TOTALAMOUNT, O.STATUS, O.ORDERDATE
            FROM ORDERS O
            JOIN CUSTOMERS C ON O.CUSTOMERID = C.CUSTOMERID
            WHERE O.ORDERDATE BETWEEN ? AND ?
            ORDER BY O.ORDERDATE DESC
        """
        return self.conn.query(sql, (start_date, end_date))

    # 8. Lịch sử cập nhật
    def add_order_history(self, order_id, user_id, action, old_value, new_value):
        sql = """
            INSERT INTO ORDERHISTORY (ORDERID, USERID, ACTION, OLDVALUE, NEWVALUE, CHANGEDATE)
            VALUES (?, ?, ?, ?, ?, GETDATE())
        """
        self.conn.query(sql, (order_id, user_id, action, old_value, new_value))

    def get_order_history(self, order_id):
        sql = """
            SELECT U.USERNAME, OH.ACTION, OH.OLDVALUE, OH.NEWVALUE, OH.CHANGEDATE
            FROM ORDERHISTORY OH
            JOIN USERS U ON OH.USERID = U.USERID
            WHERE OH.ORDERID = ?
            ORDER BY OH.CHANGEDATE DESC
        """
        return self.conn.query(sql, (order_id,))