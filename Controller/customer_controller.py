from model.customer_model import CustomerModel
from view.customer_view import CustomerView

class CustomerController:
    def __init__(self):
        self.model = CustomerModel()
        self.view = CustomerView()

    # 1. Xem danh sách khách hàng
    def list_customers(self):
        customers = self.model.get_all_customers()
        self.view.show_customer_list(customers)
        return customers

    # 2. Thêm khách hàng mới
    def add_customer(self, username, fullname, email, phone, address, id_card):
        try:
            result = self.model.add_customer(username, fullname, email, phone, address, id_card)
            if result:
                self.view.show_message("Thêm khách hàng thành công!")
            else:
                self.view.show_message("Không thể thêm khách hàng!")
        except Exception as e:
            self.view.show_error(str(e))

    def check_username_exists(self, username):
        try:
            return self.model.check_username_exists(username)
        except Exception as e:
            self.view.show_error(str(e))
            return False

    def check_email_exists(self, email):
        try:
            return self.model.check_email_exists(email)
        except Exception as e:
            self.view.show_error(str(e))
            return False

    def check_phone_exists(self, phone):
        return self.model.check_phone_exists(phone)

    # 3. Cập nhật khách hàng
    def update_customer(self, cid, fullname, email, phone, address, id_card):
        result = self.model.update_customer(cid, fullname, email, phone, address, id_card)
        if result:
            self.view.show_message("Cập nhật khách hàng thành công!")
        else:
            self.view.show_message("Không tìm thấy khách hàng để cập nhật!")

    # 4. Xóa khách hàng
    def delete_customer(self, cid):
        result = self.model.delete_customer(cid)
        if result == "constraint":
            self.view.show_message(f"Không thể xóa khách hàng ID = {cid} vì đang có đơn hàng liên kết.")
            return False
        elif result == "error":
            self.view.show_message("Lỗi hệ thống khi xóa khách hàng.")
            return False
        elif result == 0:
            self.view.show_message("Không tìm thấy khách hàng để xóa!")
            return False
        else:
            self.view.show_message("Đã xóa khách hàng thành công!")
            return True

    # 5. Xem chi tiết khách hàng theo ID
    def view_customer(self, cid):
        customer = self.model.get_customer_by_id(cid)
        self.view.show_customer_detail(customer)
        return customer

    # 6. Khóa/Mở khóa khách hàng
    def set_customer_status(self, cid, status):
        result = self.model.set_status(cid, status)
        if not (result and result > 0):
            self.view.show_message("Không tìm thấy customer để cập nhật trạng thái!")

    # 7. Tìm khách hàng theo tên/SĐT/Email
    def search_customer(self, keyword):
        customers = self.model.search_customer(keyword)
        return customers

    # 8. Thống kê
    def statistics(self):
        total = self.model.count_customers()
        active = self.model.count_by_status(1)
        locked = self.model.count_by_status(0)
        self.view.show_statistics(total, active, locked)

    # 9. Khách hàng mới nhất
    def latest_customer(self):
        customer = self.model.latest_customer()
        self.view.show_customer_detail(customer)