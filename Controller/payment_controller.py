from decimal import Decimal
from model.payment_model import PaymentModel
from view.payment_view import PaymentView


class PaymentController:
    def __init__(self):
        self.model = PaymentModel()
        self.view = PaymentView()

    # 1. Danh sách thanh toán
    def list_payments(self):
        payments = self.model.get_all()
        self.view.show_list(payments)

    # 2. Thêm thanh toán
    def add_payment(self, order_id, amount, method, transaction_id, status):
        return self.model.insert(order_id, amount, method, transaction_id, status)

    def has_payment(self, order_id):
        return self.model.has_payment(order_id)

    # 3. Cập nhật thanh toán
    def update_payment(self, payment_id, amount, method, status):
        return self.model.update(payment_id, amount, method, status)

    def validate_payment_amount(self, order_id, payment_id, new_amount):
        order = self.model.get_order_total(order_id)
        if not order:
            return False, "Không tìm thấy đơn hàng!"
        total_order_amount = order[0]  # Decimal

        payments = self.model.get_payments_by_order(order_id)
        if not payments:
            return False, "Đơn hàng chưa có thanh toán nào!"

        new_amount = Decimal(str(new_amount))  # ép float sang Decimal

        if len(payments) == 1:
            if new_amount != total_order_amount:
                return False, f"Số tiền phải đúng bằng {total_order_amount}!"
        else:
            current_total = sum(p[1] for p in payments if p[0] != payment_id)  # p[1] là Decimal
            if current_total + new_amount != total_order_amount:
                return False, f"Tổng các thanh toán phải bằng {total_order_amount}!"

        return True, None

    def show_payment_detail(self, payment):
        self.view.show_detail(payment)

    def get_payment(self, payment_id):
        return self.model.get_by_id(payment_id)

    # 4. Xóa thanh toán
    def delete_payment(self, payment_id):
        return self.model.delete(payment_id)

    # 5. Tìm kiếm thanh toán
    def search_payments(self, keyword):
        return self.model.search(keyword)

    # 6. Xuất báo cáo CSV
    def get_all_payments(self):
        return self.model.get_all()

    # 7. Lọc theo trạng thái
    def filter_status(self, status):
        return self.model.filter_by_status(status)

    # 8. Thống kê thanh toán
    def payment_stats(self):
        return self.model.stats_total_amount()
