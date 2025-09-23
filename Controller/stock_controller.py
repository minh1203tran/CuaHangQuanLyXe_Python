from model.stock_model import StockModel
from view.stock_view import StockView

class StockController:
    def __init__(self):
        self.model = StockModel()
        self.view = StockView()

    # 1. Xem danh sách tồn kho
    # def list_stocks(self):
    #     stocks = self.model.get_all()
    #     self.view.show_stock_list(stocks)

    def list_stocks(self, show=True):
        stocks = self.model.get_all()
        if show:
            self.view.show_stock_list(stocks)
        return stocks

    # 2. Thêm tồn kho mới
    def add_stock(self, vehicle_id, quantity, min_quantity):
        if self.model.exists(vehicle_id):
            return False
        return self.model.insert(vehicle_id, quantity, min_quantity)

    # 3. Cập nhật tồn kho
    def update_stock(self, stock_id, qty, min_level):
        result = self.model.update(stock_id, qty, min_level)
        if result:
            self.view.show_message("Cập nhật tồn kho thành công!")
        else:
            self.view.show_message("Cập nhật tồn kho thất bại!")

    # 4. Xóa tồn kho
    def delete_stock(self, stock_id):
        result = self.model.delete(stock_id)
        if result:
            self.view.show_message("Xóa tồn kho thành công!")
        else:
            self.view.show_message("Xóa tồn kho thất bại!")

    # 5. Tìm kiếm tồn kho theo xe
    def search_stock(self, keyword):
        return self.model.search_by_vehicle(keyword)

    # 6. Báo cáo tồn dưới mức tối thiểu
    def report_below_min(self):
        return self.model.report_below_min()

    # 7. Báo cáo xe âm
    def report_negative_stock(self):
        return self.model.report_negative_stock()

    # 8. Xuất kho nhanh
    def stock_out(self, stock_id, qty):
        return self.model.stock_out(stock_id, qty)

    # 9. Xuất báo cáo CSV
    def get_all_stocks(self):
        return self.model.get_all()