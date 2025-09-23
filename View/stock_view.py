class StockView:
    @staticmethod
    def show_stock_list(stocks):
        if not stocks:
            print("Không có dữ liệu tồn kho!")
            return

        print("\n===== DANH SÁCH TỒN KHO =====")
        for s in stocks:
            print(f"ID kho: {s[0]} | ID xe: {s[1]} | Xe: {s[2]} - {s[3]} | "
                  f"Số lượng: {s[4]} | Tồn tối thiểu: {s[5]} | Ngày nhập gần nhất: {s[6]}")

    @staticmethod
    def show_message(msg):
        print(msg)
