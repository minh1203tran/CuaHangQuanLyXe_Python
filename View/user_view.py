class UserView:
    @staticmethod
    def show_user_list(users):
        if not isinstance(users, list):
            users = [users]
        print("--- DANH SÁCH USER ---")
        for u in users:
            print(f"ID: {u[0]} | Username: {u[1]} | Họ tên: {u[2]} | Vai trò: {u[3]} | Ngày tạo: {u[4]}")

    @staticmethod
    def show_user_detail(user):
        if user:
            print("\n--- THÔNG TIN USER ---")
            print(f"ID: {user[0]}")
            print(f"Username: {user[1]}")
            print(f"Password: {user[2]}")
            print(f"Họ tên: {user[3]}")
            print(f"Vai trò: {user[4]}")
            print(f"Ngày tạo: {user[5]}")
        else:
            print("Không tìm thấy user.")

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_error(err):
        print(f"{err}")