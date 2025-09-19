import re
import unicodedata
from controller.customer_controller import CustomerController

class CustomerApp:
    def __init__(self):
        self.controller = CustomerController()

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

    def validate_email(self, email: str) -> bool:
        if " " in email:
            return False
        if "_" in email or "-" in email:
            return False
        normalized = unicodedata.normalize("NFD", email)
        for ch in normalized:
            if unicodedata.category(ch) == "Mn":
                return False
        pattern = r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.(com|vn)$'
        return re.match(pattern, email) is not None

    def is_valid_username(self, username: str) -> bool:
        if " " in username:
            return False
        normalized = unicodedata.normalize("NFD", username)
        for ch in normalized:
            if unicodedata.category(ch) == "Mn":
                return False
        pattern = r'^[A-Za-z0-9]+$'
        return re.match(pattern, username) is not None

    # 1. Xem danh sách khách hàng
    def hien_thi_ds_customer(self):
        self.controller.list_customers()

    # 2. Thêm khách hàng mới
    def them_customer_moi(self):
        print("--- Thêm khách hàng mới (Nhấn 0 để hủy) ---")
        while True:
            username = self.get_input("Username (không dấu, không cách): ")
            if username is None:
                return
            if not username.strip():
                print("Username không được để trống!")
                continue
            if not self.is_valid_username(username):
                print("Username chỉ được chứa chữ cái không dấu, số.")
                continue
            if self.controller.check_username_exists(username):
                print(f"Username '{username}' đã tồn tại! Vui lòng chọn username khác.")
                continue
            break
        while True:
            fullname = self.get_input("Họ tên: ")
            if fullname is None:
                return
            if not fullname.strip():
                print("Họ tên không được để trống!")
                continue
            break
        while True:
            email = self.get_input("Email: ")
            if email is None:
                return
            if not self.validate_email(email):
                print("Email không hợp lệ! Phải có '@' và kết thúc bằng .com hoặc .vn, đồng thời có ký tự trước đuôi.")
                continue
            if self.controller.check_email_exists(email):
                print(f"Email '{email}' đã tồn tại! Vui lòng nhập email khác.")
                continue
            break
        while True:
            phone = self.get_input("Số điện thoại (10 số): ")
            if phone is None:
                return
            if not (phone.isdigit() and len(phone) == 10):
                print("Số điện thoại không hợp lệ! Vui lòng nhập đúng 10 chữ số.")
                continue
            break
        while True:
            address = self.get_input("Địa chỉ: ")
            if address is None:
                return
            if not address.strip():
                print("Địa chỉ không được để trống!")
                continue
            break
        while True:
            id_card = self.get_input("Số CCCD (12 số): ")
            if id_card is None:
                return
            if not id_card.strip():
                print("Số CCCD không được để trống!")
                continue
            if not (id_card.isdigit() and len(id_card) == 12):
                print("Số CCCD phải gồm đúng 12 chữ số!")
                continue
            break
        self.controller.add_customer(username, fullname, email, phone, address, id_card)

    # 3. Cập nhật khách hàng
    def cap_nhat_customer(self):
        self.controller.list_customers()
        while True:
            cid = self.get_input("\nNhập ID Customer cần cập nhật (0 để hủy): ", cast_func=int)
            if cid is None or cid == 0:
                return
            current = self.controller.view_customer(cid)
            if not current:
                continue
            break
        print("\n--- Nhập thông tin mới (Enter để giữ nguyên) ---")
        fullname = self.get_input("Họ tên mới: ", default=current[2])
        if fullname is None:
            return
        while True:
            email = input(f"Email mới (Enter để giữ nguyên: {current[3]}): ").strip()
            if email == "":
                email = current[3]
                break
            if not self.validate_email(email):
                print("Email không hợp lệ! Phải có '@' và kết thúc bằng .com hoặc .vn.")
                continue
            if self.controller.check_email_exists(email) and email != current[3]:
                print(f"Email '{email}' đã tồn tại! Vui lòng nhập email khác.")
                continue
            break
        while True:
            phone = input(f"Số điện thoại mới (Enter để giữ nguyên: {current[4]}): ").strip()
            if phone == "":
                phone = current[4]
                break
            if not (phone.isdigit() and len(phone) == 10):
                print("Số điện thoại không hợp lệ! Phải đủ 10 chữ số.")
                continue
            if self.controller.check_phone_exists(phone) and phone != current[4]:
                print(f"Số điện thoại '{phone}' đã tồn tại! Vui lòng nhập số khác.")
                continue
            break
        address = self.get_input("Địa chỉ mới: ", default=current[5])
        if address is None:
            return
        while True:
            id_card = input(f"CCCD mới (Enter để giữ nguyên: {current[6]}): ").strip()
            if id_card == "":
                id_card = current[6]
                break
            if not (id_card.isdigit() and len(id_card) == 12):
                print("Số CCCD phải gồm đúng 12 chữ số!")
                continue
            break
        while True:
            confirm = input("Bạn có chắc chắn muốn cập nhật customer này? (Y/N): ").strip().upper()
            if confirm in ["Y", "N"]:
                break
            print("Vui lòng nhập Y (đồng ý) hoặc N (hủy).")
        if confirm == "Y":
            self.controller.update_customer(cid, fullname, email, phone, address, id_card)
        else:
            print("Hủy cập nhật khách hàng.")

    # 4. Xóa khách hàng
    def xoa_customer(self):
        self.controller.list_customers()
        while True:
            cid = self.get_input("\nNhập ID Customer cần xóa (0 để hủy): ", cast_func=int)
            if cid is None or cid == 0:
                return
            cus = self.controller.view_customer(cid)
            if not cus:
                continue
            confirm = input(f"\nBạn có CHẮC CHẮN muốn xóa Customer này? (Y/N): ").strip().upper()
            if confirm == "Y":
                self.controller.delete_customer(cid)
            else:
                print("Hủy thao tác xóa.")
            break

    # 5. Xem chi tiết khách hàng theo ID
    def xem_chi_tiet_customer(self):
        self.controller.list_customers()
        while True:
            cid = self.get_input("\nNhập ID khách hàng (0 để hủy): ", cast_func=int)
            if cid is None or cid == 0:
                return
            cus = self.controller.view_customer(cid)
            if cus:
                break

    # 6. Khóa/Mở khóa khách hàng
    def khoa_mo_khoa_customer(self):
        self.controller.list_customers()
        while True:
            cid = self.get_input("\nNhập ID Customer cần khóa/mở khóa (0 để hủy): ", cast_func=int)
            if cid is None or cid == 0:
                return
            cus = self.controller.view_customer(cid)
            if not cus:
                continue
            break
        while True:
            try:
                action = int(input("Nhập (1: mở khóa, 0: khóa): ").strip())
                if action not in [0, 1]:
                    print("Chỉ được nhập 0 hoặc 1!")
                    continue
            except ValueError:
                print("Vui lòng nhập số 0 hoặc 1!")
                continue
            status = 1 if action == 1 else 0
            self.controller.set_customer_status(cid, status)
            print("Khách hàng đã được", "mở khóa." if status == 1 else "khóa.")
            break

    # 7. Tìm khách hàng theo tên/SĐT/Email
    def tim_customer(self):
        keyword = self.get_input("Nhập tên/SĐT/Email cần tìm (0 để hủy): ")
        if keyword is None or keyword == "0":
            return
        results = self.controller.search_customer(keyword)
        if results:
            print("\n--- KẾT QUẢ TÌM KIẾM ---")
            for row in results:
                print(f"ID: {row[0]} | Username: {row[1]} | Họ tên: {row[2]} | "
                      f"Email: {row[3]} | Phone: {row[4]} | "
                      f"Trạng thái: {'Hoạt động' if row[8] == 1 else 'Khóa'}")
        else:
            print("Không tìm thấy khách hàng nào.")

    # 8. Thống kê
    def thong_ke_customer(self):
        try:
            self.controller.statistics()
        except Exception as e:
            print(f"Lỗi khi thống kê: {e}")

    # 9. Khách hàng mới nhất
    def khach_hang_moi_nhat(self):
        try:
            self.controller.latest_customer()
        except Exception as e:
            print(f"Lỗi khi lấy khách hàng mới nhất: {e}")