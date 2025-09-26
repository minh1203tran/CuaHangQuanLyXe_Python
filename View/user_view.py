class UserView:
    @staticmethod
    def show_user_list(users):
        if not isinstance(users, list):
            users = [users]
        print("--- DANH SÁCH NGƯỜI DÙNG ---")
        for u in users:
            print(f"ID người dùng: {u[0]} | Tên người dùng: {u[1]} | Họ & tên: {u[2]} | Vai trò: {u[3]} | Ngày tạo: {u[4]}")

    @staticmethod
    def show_user_detail(user):
        if user:
            print("--- THÔNG TIN NGƯỜI DÙNG ---")
            print(f"ID người dùng: {user[0]}")
            print(f"Tên người dùng: {user[1]}")
            print(f"Mật khẩu: {user[2]}")
            print(f"Họ & tên: {user[3]}")
            print(f"Vai trò: {user[4]}")
            print(f"Ngày tạo: {user[5]}")
        else:
            print("Không tìm thấy người dùng.")

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_error(err):
        print(f"{err}")