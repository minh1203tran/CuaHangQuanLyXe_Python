from MSSQLServer.MSSQLServer import Database

class UserModel:
    def __init__(self):
        self.conn = Database.get_instance()

    # 1. Xem danh sách User
    def get_all_users(self):
        sql = "SELECT USERID, USERNAME, FULLNAME, ROLE, CREATED_AT FROM USERS"
        return self.conn.query(sql)

    # 2. Thêm User mới
    def add_user(self, username, password, fullname, role):
        sql = "INSERT INTO USERS (USERNAME, PASSWORD, FULLNAME, ROLE) VALUES (?, ?, ?, ?)"
        return self.conn.query(sql, (username, password, fullname, role))

    #  3. Cập nhật User
    def update_user(self, uid, fullname, role, password=None):
        if password:
            sql = "UPDATE USERS SET FULLNAME=?, ROLE=?, PASSWORD=? WHERE USERID=?"
            return self.conn.query(sql, (fullname, role, password, uid))
        else:
            sql = "UPDATE USERS SET FULLNAME=?, ROLE=? WHERE USERID=?"
            return self.conn.query(sql, (fullname, role, uid))

    # 4. Xóa User
    def delete_user(self, uid):
        sql = "DELETE FROM USERS WHERE USERID = ?"
        return self.conn.query(sql, (uid,))

    # 5. Xem chi tiết User theo ID
    def get_user_by_id(self, user_id):
        sql = "SELECT * FROM USERS WHERE USERID = ?"
        result = self.conn.query(sql, (user_id,))
        return result[0] if result else None

    # 6. Đăng nhập
    def login(self, username, password):
        sql = "SELECT USERID, USERNAME, FULLNAME, ROLE FROM USERS WHERE USERNAME=? AND PASSWORD=?"
        result = self.conn.query(sql, (username, password))
        return result[0] if result else None

    # 7. Đổi mật khẩu
    def change_password(self, uid, new_password):
        sql = "UPDATE USERS SET PASSWORD=? WHERE USERID=?"
        return self.conn.query(sql, (new_password, uid))

    # 8. Tìm kiếm User
    # def find_user(self, username=None, fullname=None):
    #     if username:
    #         sql = "SELECT USERID, USERNAME, FULLNAME, ROLE, CREATED_AT FROM USERS WHERE USERNAME LIKE ?"
    #         return self.conn.query(sql, (f"%{username}%",))
    #     elif fullname:
    #         sql = "SELECT USERID, USERNAME, FULLNAME, ROLE, CREATED_AT FROM USERS WHERE FULLNAME LIKE ?"
    #         return self.conn.query(sql, (f"%{fullname}%",))
    #     return None

    def find_user(self, keyword=None):
        if not keyword:
            return []
        sql = """
            SELECT USERID, USERNAME, FULLNAME, ROLE, CREATED_AT
            FROM USERS
            WHERE USERNAME LIKE ? OR FULLNAME LIKE ?
        """
        return self.conn.query(sql, (f"%{keyword}%", f"%{keyword}%"))


