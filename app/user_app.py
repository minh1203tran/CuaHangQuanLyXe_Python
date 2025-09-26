import re
from controller.user_controller import UserController

class UserApp:
    def __init__(self):
        self.controller = UserController()

    def get_input(self, prompt, default=None, allow_quit=True, to_upper=False, validator=None, cast_func=None):
        while True:
            value = input(prompt).strip()
            if allow_quit and value.upper() == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return None
            if not value and default is not None:
                return default
            if to_upper:
                value = value.upper()
            if cast_func:
                try:
                    value = cast_func(value)
                except ValueError:
                    print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                    continue
            if validator and not validator(value):
                print("Giá trị không hợp lệ! Vui lòng nhập lại.")
                continue
            return value

    # 1. Xem danh sách User
    def hien_thi_ds_user(self):
        self.controller.list_users()

    # 2. Thêm User mới
    def them_user_moi(self):
        print("--- Thêm người dùng mới (Nhấn 0 để hủy) ---")
        while True:
            username = self.get_input("Tên đăng nhập: ", cast_func=str)
            if username is None:
                return
            if self.controller.check_username_exists(username):
                print(f"Tên đăng nhập '{username}' đã tồn tại! Vui lòng chọn tên đăng nhập khác.")
                continue
            break
        password = self.get_input("Mật khẩu: ", cast_func=str)
        if password is None:
            return
        fullname = self.get_input("Họ & tên: ", cast_func=str)
        if fullname is None:
            return
        role = self.get_input("Vai trò (ADMIN/STAFF): ", cast_func=str, to_upper=True,
                              validator=lambda r: r in ["ADMIN", "STAFF"])
        if role is None:
            return
        self.controller.add_user(username, password, fullname, role)

    #  3. Cập nhật User
    def cap_nhat_user(self):
        while True:
            uid = self.get_input("Nhập ID người dùng cần cập nhật (0 để hủy): ", cast_func=int)
            if uid is None:
                return
            if uid == 0:
                print("Đã hủy cập nhật người dùng.")
                return
            current = self.controller.show_user(uid)
            if not current:
                continue
            break
        print("--- Nhập thông tin mới (Enter để giữ nguyên, 0 để hủy) ---")
        fullname = self.get_input("Họ & tên mới: ", default=current[2])
        if fullname is None or fullname == "0":
            print("Hủy cập nhật người dùng.")
            return
        password = self.get_input("Mật khẩu mới: ", default=None)
        if password == "0":
            print("Hủy cập nhật người dùng.")
            return
        while True:
            role = self.get_input("Vai trò mới (ADMIN/STAFF, Enter để giữ nguyên, 0 để hủy): ",
                                  to_upper=True)
            if role is None:
                return
            role = role.strip().upper()
            if role == "0":
                return
            if role == "":
                role = None
                break
            if role in ["ADMIN", "STAFF"]:
                break
            print("Vai trò không hợp lệ! Chỉ chấp nhận ADMIN hoặc STAFF.")
        while True:
            confirm = input("Bạn có chắc chắn muốn cập nhật user này? (Y/N): ").strip().upper()
            if confirm == "N":
                print("Hủy cập nhật người dùng.")
                return
            if confirm == "Y":
                self.controller.update_user(uid, fullname, role, password)
                return
            print("Chỉ được nhập Y (đồng ý), N (hủy). Vui lòng nhập lại.")

    # 4. Xóa User
    def xoa_user(self):
        while True:
            uid = self.get_input("Nhập ID người dùng cần xóa (0 để hủy): ", cast_func=int)
            if uid is None or uid == 0:
                print("Hủy thao tác xóa.")
                return
            user = self.controller.show_user(uid)
            if not user:
                continue
            while True:
                confirm = input("Bạn có CHẮC CHẮN muốn xóa User này? (Y/N): ").strip().upper()
                if confirm == "Y":
                    self.controller.delete_user(uid)
                    return
                elif confirm == "N":
                    print("Hủy thao tác xóa.")
                    return
                else:
                    print("Chỉ được nhập Y hoặc N.")

    # 5. Xem chi tiết User theo ID
    def xem_chi_tiet_user(self):
        while True:
            uid = self.get_input("Nhập ID người dùng (0 để hủy): ", cast_func=int)
            if uid is None:
                return
            if uid == 0:
                return
            user = self.controller.show_user(uid)
            if user:
                break

    # 6. Đăng nhập
    def dang_nhap(self):
        print("Nhập tên đăng nhập và mật khẩu (0 để hủy).")
        username = self.get_input("Tên đăng nhập: ", cast_func=str)
        if username is None: return
        password = self.get_input("Mật khẩu: ", cast_func=str)
        if password is None: return
        self.controller.login(username, password)

    # 7. Đổi mật khẩu
    def doi_mat_khau(self):
        while True:
            keyword = self.get_input("Nhập từ khóa tìm kiếm người dùng (tên đăng nhập hoặc họ & tên, 0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return
            users = self.controller.find_user(keyword.strip())
            if not users:
                print("Không tìm thấy người dùng nào. Vui lòng thử lại hoặc nhập 0 để thoát.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM ---")
            for u in users:
                print(f"ID người dùng: {u[0]} | tên đăng nhập: {u[1]} | Họ & tên: {u[2]} | Vai trò: {u[3]} | Ngày tạo: {u[4]}")
            valid_ids = [u[0] for u in users]
            uid = None
            while uid not in valid_ids:
                uid = self.get_input("Nhập ID người dùng cần đổi mật khẩu (0 để hủy): ", cast_func=int)
                if uid is None or uid == 0:
                    return
                if uid not in valid_ids:
                    print("ID người dùng không tồn tại trong danh sách, vui lòng nhập lại!")
            new_pass = None
            while not new_pass:
                new_pass = self.get_input("Nhập mật khẩu mới (0 để hủy): ")
                if new_pass is None or new_pass.strip() == "0":
                    return
                if not new_pass.strip():
                    print("Mật khẩu không được để trống!")
                    new_pass = None
            self.controller.change_password(uid, new_pass)
            return

    # 8. Tìm kiếm User
    def tim_kiem_user(self):
        while True:
            keyword = self.get_input("Nhập từ khóa tìm kiếm (Tên đăng nhập hoặc họ & tên, nhập 0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                break
            users = self.controller.find_user(keyword)
            if users:
                print("--- KẾT QUẢ TÌM KIẾM ---")
                for u in users:
                    print(f"ID người dùng: {u[0]} | Tên đăng nhập: {u[1]} | Họ & tên: {u[2]} | "
                          f"Vai trò: {u[3]} | Ngày tạo: {u[4]}")
                print()
                break
            else:
                print("Không tìm thấy người dùng nào. Vui lòng thử lại hoặc nhập 0 để thoát.")
