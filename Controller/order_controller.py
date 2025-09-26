from model.order_model import OrderModel
from view.order_view import OrderView

class OrderController:
    def __init__(self):
        self.model = OrderModel()
        self.view = OrderView()

    # 1. Xem danh sách đơn hàng
    def list_orders(self):
        orders = self.model.get_all_orders()
        self.view.show_orders(orders)
        return orders

    # 2. Xem chi tiết đơn hàng
    def view_order(self, order_id):
        order = self.model.get_order_by_id(order_id)
        if not order:
            self.view.show_message("Không tìm thấy đơn hàng!")
            return None
        self.view.show_orders([order])
        details = self.model.get_order_details(order_id)
        self.view.show_order_details(details)
        return order

    # 3. Tạo đơn hàng mới
    def add_order(self, customer_id, user_id, payment_method, delivery_address, note, order_items):
        try:
            self.model.add_order(customer_id, user_id, payment_method, delivery_address, note)
            order = self.model.latest_order()
            order_id = order[0]
            for item in order_items:
                self.model.add_order_detail(order_id, item['vehicle_id'], item['quantity'], item['unit_price'])
            self.view.show_message("Tạo đơn hàng thành công!")
        except Exception as e:
            self.view.show_error(str(e))

    # 4. Cập nhật trạng thái đơn hàng
    def update_order_status_and_get_old(self, order_id, new_status):
        old_status, _ = self.model.update_order_status(order_id, new_status)
        return old_status, new_status

    # 5. Tìm kiếm đơn hàng
    def search_orders(self, keyword=None, limit=20):
        return self.model.search_orders(keyword, limit)

    # 6. Thống kê đơn hàng
    def get_orders_by_status(self, status):
        return self.model.get_orders_by_status(status)

    def get_sales_statistics(self, period='month'):
        return self.model.get_sales_statistics(period)

    def get_orders_by_date_range(self, start_date, end_date):
        return self.model.get_orders_by_date_range(start_date, end_date)

    # 7. In hóa đơn
    def print_invoice(self, order_id):
        order = self.model.get_order_by_id(order_id)
        if not order:
            self.view.show_message("Không tìm thấy đơn hàng!")
            return None

        details = self.model.get_order_details(order_id)
        return order, details

    # 8. Lịch sử cập nhật
    def get_order_history(self, order_id):
        return self.model.get_order_history(order_id)

    def add_order_history(self, order_id, user_id, action, old_value, new_value):
        self.model.add_order_history(order_id, user_id, action, old_value, new_value)

    def get_order_total(self, order_id):
        return self.model.get_order_total(order_id)
