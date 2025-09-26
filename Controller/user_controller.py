from model.user_model import UserModel
from view.user_view import UserView

class UserController:
    def __init__(self):
        self.model = UserModel()
        self.view = UserView()

    # 1. Xem danh sách User
    def list_users(self):
        users = self.model.get_all_users()
        if not users:
            self.view.show_message("Không có user nào trong hệ thống!")
        else:
            self.view.show_user_list(users)

    # 2. Thêm User mới
    def add_user(self, username, password, fullname, role):
        if self.check_username_exists(username):
            self.view.show_error(f"Username '{username}' đã tồn tại!")
            return False
        result = self.model.add_user(username, password, fullname, role)
        if result:
            self.view.show_message("Thêm user thành công!")
            return True
        else:
            self.view.show_error("Không thể thêm user.")
            return False

    def check_username_exists(self, username: str) -> bool:
        sql = "SELECT COUNT(*) FROM USERS WHERE USERNAME = ?"
        result = self.model.conn.query(sql, (username,))
        return result[0][0] > 0 if result else False

    #  3. Cập nhật User
    def update_user(self, uid, fullname, role, password=None):
        result = self.model.update_user(uid, fullname, role, password)
        if result:
            self.view.show_message("Cập nhật người dùng thành công!")
        else:
            self.view.show_error("Không thể cập nhật người dùng.")

    # 4. Xóa User
    def delete_user(self, user_id):
        result = self.model.delete_user(user_id)
        if result == "constraint":
            print(f"Không thể xóa người dùng ID = {user_id} vì đang có đơn hàng liên kết.")
            return False
        elif result == "error":
            print("Lỗi hệ thống khi xóa người dùng.")
            return False
        elif result == 0:
            print(f"Không tìm thấy người dùng ID = {user_id} để xóa.")
            return False
        elif result > 0:
            print("Đã xóa User thành công.")
            return True

    # 5. Xem chi tiết User theo ID
    def show_user(self, user_id):
        user = self.model.get_user_by_id(user_id)
        if user:
            self.view.show_user_detail(user)
            return user
        else:
            self.view.show_error("Không tìm thấy người dùng.")
            return None

    # 6. Đăng nhập
    def login(self, username, password):
        user = self.model.login(username, password)
        if user:
            self.view.show_message(f"Đăng nhập thành công! Xin chào {user[2]} ({user[1]})")
            return user
        else:
            self.view.show_error("Sai username hoặc password!")
            return None

    # 7. Đổi mật khẩu
    def change_password(self, uid, new_password):
        result = self.model.change_password(uid, new_password)
        if result and result > 0:
            self.view.show_message("Đổi mật khẩu thành công!")

    # 8. Tìm kiếm User
    def find_user(self, keyword=None):
        users = self.model.find_user(keyword)
        if users and len(users) > 0:
            return users
        return []


