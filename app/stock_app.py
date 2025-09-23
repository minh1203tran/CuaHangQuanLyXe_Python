import csv
import os
from controller.stock_controller import StockController
from controller.vehicle_controller import VehicleController

class StockApp:
    def __init__(self):
        self.controller = StockController()
        self.vehicle = VehicleController()

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

    # 1. Xem danh sách tồn kho
    def hien_thi_ds_stock(self):
        self.controller.list_stocks()

    # 2. Thêm tồn kho mới
    def them_stock_moi(self):
        while True:
            keyword = self.get_input("Nhập hãng xe (0 để hủy): ", allow_quit=True)
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm! Vui lòng nhập lại.")
                continue
            vehicles = self.vehicle.search_by_manufacturer(keyword)
            if not vehicles:
                print("Không tìm thấy xe nào! Vui lòng thử lại.")
                continue
            print("--- DANH SÁCH XE TÌM ĐƯỢC ---")
            for v in vehicles:
                print(f"ID: {v[0]} | Biển số: {v[1]} | Dòng xe: {v[2]} | Hãng xe: {v[3]} | Giá: {v[6]}")
            while True:
                vehicle_id = self.get_input("Chọn ID xe từ danh sách (0 để hủy): ",
                                            allow_quit=True, cast_func=int)
                if vehicle_id is None:
                    return
                if vehicle_id in [v[0] for v in vehicles]:
                    if self.controller.model.exists(vehicle_id):
                        print("Xe này đã có trong kho! Vui lòng cập nhật thay vì thêm mới.")
                        chosen_vehicle = None
                        break
                    chosen_vehicle = next(v for v in vehicles if v[0] == vehicle_id)
                    print("--- XÁC NHẬN XE ---")
                    print(f"ID: {chosen_vehicle[0]} | Biển số: {chosen_vehicle[1]} | "
                          f"Dòng xe: {chosen_vehicle[2]} | Hãng xe: {chosen_vehicle[3]} | Giá: {chosen_vehicle[6]}")
                    confirm = self.get_input("Xe bạn nhập đúng chưa? (y/n, 0 để hủy): ",
                                             allow_quit=True, to_upper=True)
                    if confirm is None:
                        return
                    if confirm == "Y":
                        break
                    elif confirm == "N":
                        chosen_vehicle = None
                        print("Quay lại tìm kiếm xe từ đầu.")
                        break
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")
                        continue
                else:
                    print("ID xe không nằm trong danh sách bạn tìm! Vui lòng nhập lại.")
            if not chosen_vehicle:
                continue
            while True:
                qty_str = self.get_input("Nhập số lượng tồn (0 để hủy): ", allow_quit=True)
                if qty_str is None:
                    return
                if not str(qty_str).strip():
                    print("Bạn phải nhập số lượng tồn! Vui lòng nhập lại.")
                    continue
                try:
                    qty = int(qty_str)
                    break
                except ValueError:
                    print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
            while True:
                min_str = self.get_input("Nhập mức tồn tối thiểu (0 để hủy): ", allow_quit=True)
                if min_str is None:
                    return
                if not str(min_str).strip():
                    print("Bạn phải nhập mức tồn tối thiểu! Vui lòng nhập lại.")
                    continue
                try:
                    min_level = int(min_str)
                    if min_level < 0:
                        print("Mức tồn tối thiểu không được âm! Vui lòng nhập lại.")
                        continue
                    break
                except ValueError:
                    print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
            if self.controller.add_stock(chosen_vehicle[0], qty, min_level):
                print("Thêm tồn kho thành công!")
                return

    # 3. Cập nhật tồn kho
    def cap_nhat_stock(self):
        while True:
            keyword = self.get_input("Nhập hãng xe để tìm kho (0 để hủy): ", allow_quit=True)
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm!")
                continue
            stocks = self.controller.search_stock(keyword)
            if not stocks:
                print("Không tìm thấy xe nào trong kho! Vui lòng thử lại.")
                continue
            print("--- DANH SÁCH TỒN KHO ---")
            for s in stocks:
                print(f"ID kho: {s[0]} | ID xe: {s[1]} | Biển số: {s[2]} | "
                      f"Dòng xe: {s[3]} | Hãng: {s[4]} | "
                      f"Số lượng: {s[5]} | Tồn tối thiểu: {s[6]} | Ngày nhập: {s[7]}")
            while True:
                stock_id = self.get_input("Chọn ID kho để cập nhật (0 để hủy): ",
                                          allow_quit=True, cast_func=int)
                if stock_id is None:
                    return
                chosen_stock = next((s for s in stocks if s[0] == stock_id), None)
                if not chosen_stock:
                    print("ID kho không hợp lệ! Vui lòng nhập lại.")
                    continue
                print("--- XÁC NHẬN KHO ---")
                print(f"ID kho: {chosen_stock[0]} | ID xe: {chosen_stock[1]} | "
                      f"Biển số: {chosen_stock[2]} | Dòng xe: {chosen_stock[3]} | "
                      f"Hãng: {chosen_stock[4]} | Số lượng: {chosen_stock[5]} | Mức tồn tối thiểu: {chosen_stock[6]}")
                while True:
                    confirm = self.get_input("Bạn có chắc muốn cập nhật kho này? (y/n, 0 để hủy): ",
                                             allow_quit=True, to_upper=True)
                    if confirm is None:
                        return
                    if confirm == "N":
                        print("Hủy cập nhật. Quay lại tìm kho.")
                        break
                    elif confirm == "Y":
                        break
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")
                while True:
                    qty_str = self.get_input(f"Nhập số lượng mới (0 để hủy, Enter để giữ {chosen_stock[5]}): ",
                                             allow_quit=True)
                    if qty_str is None:
                        return
                    if qty_str.strip() == "":
                        qty = chosen_stock[5]
                        break
                    try:
                        qty = int(qty_str)
                        break
                    except ValueError:
                        print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                while True:
                    min_str = self.get_input(f"Nhập mức tồn tối thiểu mới (0 để hủy, Enter để giữ {chosen_stock[6]}): ",
                                             allow_quit=True)
                    if min_str is None:
                        return
                    if min_str.strip() == "":
                        min_level = chosen_stock[6]
                        break
                    try:
                        min_level = int(min_str)
                        if min_level < 0:
                            print("Mức tồn tối thiểu không được âm! Vui lòng nhập lại.")
                            continue
                        break
                    except ValueError:
                        print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                success = self.controller.update_stock(stock_id, qty, min_level)
                if success:
                    print("Cập nhật tồn kho thành công!")
                return

    # 4. Xóa tồn kho
    def xoa_stock(self):
        while True:
            keyword = self.get_input("Nhập hãng xe để tìm kho (0 để hủy): ", allow_quit=True)
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm!")
                continue
            stocks = self.controller.search_stock(keyword)
            if not stocks:
                print("Không tìm thấy xe nào trong kho! Vui lòng thử lại.")
                continue

            print("--- DANH SÁCH TỒN KHO ---")
            for s in stocks:
                print(f"ID kho: {s[0]} | ID xe: {s[1]} | Biển số: {s[2]} | "
                      f"Dòng xe: {s[3]} | Hãng: {s[4]} | "
                      f"Số lượng: {s[5]} | Tồn tối thiểu: {s[6]} | Ngày nhập: {s[7]}")
            while True:
                stock_id = self.get_input("Chọn ID kho để xóa (0 để hủy): ", allow_quit=True, cast_func=int)
                if stock_id is None:
                    return
                chosen_stock = next((s for s in stocks if s[0] == stock_id), None)
                if not chosen_stock:
                    print("ID kho không hợp lệ! Vui lòng nhập lại.")
                    continue
                print("--- XÁC NHẬN XÓA ---")
                print(f"ID kho: {chosen_stock[0]} | ID xe: {chosen_stock[1]} | Biển số: {chosen_stock[2]} | "
                      f"Dòng xe: {chosen_stock[3]} | Hãng: {chosen_stock[4]} | Số lượng: {chosen_stock[5]} | Mức tồn tối thiểu: {chosen_stock[6]}")
                while True:
                    confirm = self.get_input("Bạn có chắc muốn xóa kho này? (y/n, 0 để hủy): ",
                                             allow_quit=True, to_upper=True)
                    if confirm is None or confirm == "0":
                        return
                    elif confirm == "N":
                        print("Hủy xóa. Quay lại tìm kho.")
                        break
                    elif confirm == "Y":
                        self.controller.delete_stock(stock_id)
                        return
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")

    # 5. Tìm kiếm tồn kho theo xe
    def tim_kiem_stock(self):
        while True:
            keyword = self.get_input("Nhập hãng xe để tìm kho (0 để hủy): ", allow_quit=True)
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm!")
                continue
            stocks = self.controller.search_stock(keyword)
            if not stocks:
                print("Không tìm thấy xe nào trong kho! Vui lòng thử lại.")
                continue
            print("--- DANH SÁCH TỒN KHO ---")
            for s in stocks:
                print(f"ID kho: {s[0]} | ID xe: {s[1]} | Biển số: {s[2]} | "
                      f"Dòng xe: {s[3]} | Hãng: {s[4]} | "
                      f"Số lượng: {s[5]} | Mức tồn tối thiểu: {s[6]} | Ngày nhập: {s[7]}")
            break

    # 6. Báo cáo tồn dưới mức tối thiểu
    def bao_cao_below_min(self):
        data = self.controller.report_below_min()
        if not data:
            print("Không có xe nào dưới mức tồn tối thiểu.")
            return
        print("--- XE DƯỚI MỨC TỒN TỐI THIỂU ---")
        for s in data:
            print(f"ID kho: {s[0]} | Dòng xe: {s[1]} | Hãng xe: {s[2]} | Số lượng: {s[3]} | Mức tồn tối thiểu: {s[4]}")

    # 7. Báo cáo xe âm
    def bao_cao_negative(self):
        data = self.controller.report_negative_stock()
        if not data:
            print("Không có xe nào âm.")
            return
        print("--- XE CÓ SỐ LƯỢNG ÂM ---")
        for s in data:
            print(f"ID kho: {s[0]} | Dòng xe: {s[1]} | Hãng: {s[2]} | Số lượng: {s[3]}")

    # 8. Xuất kho nhanh
    def xuat_kho_nhanh(self):
        while True:
            keyword = self.get_input("Nhập hãng xe để tìm kho (0 để hủy): ", allow_quit=True)
            if keyword is None:
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm!")
                continue
            stocks = self.controller.search_stock(keyword)
            if not stocks:
                print("Không tìm thấy xe nào trong kho! Vui lòng thử lại.")
                continue
            print("--- DANH SÁCH TỒN KHO ---")
            for s in stocks:
                print(f"ID kho: {s[0]} | ID xe: {s[1]} | Biển số: {s[2]} | "
                      f"Dòng xe: {s[3]} | Hãng: {s[4]} | "
                      f"Số lượng: {s[5]} | Tồn tối thiểu: {s[6]} | Ngày nhập: {s[7]}")
            while True:
                stock_id = self.get_input("Chọn ID kho để xuất (0 để hủy): ", allow_quit=True, cast_func=int)
                if stock_id is None:
                    return
                chosen_stock = next((s for s in stocks if s[0] == stock_id), None)
                if not chosen_stock:
                    print("ID kho không hợp lệ! Vui lòng nhập lại.")
                    continue
                while True:
                    qty = self.get_input("Nhập số lượng xuất (0 để hủy): ", allow_quit=True, cast_func=int)
                    if qty is None:
                        return
                    if qty <= 0:
                        print("Số lượng xuất phải lớn hơn 0!")
                        continue
                    if qty > chosen_stock[5]:
                        print(f"Không thể xuất {qty} xe. Tồn kho hiện tại chỉ còn {chosen_stock[5]}.")
                        continue
                    break
                print("--- XÁC NHẬN XUẤT ---")
                print(f"Kho {chosen_stock[0]} | Xe {chosen_stock[3]} - {chosen_stock[4]} "
                      f"| Số lượng hiện tại: {chosen_stock[5]} | Xuất: {qty}")
                while True:
                    confirm = input("Bạn có chắc muốn xuất kho này? (y/n, 0 để hủy): ").strip().lower()
                    if confirm == "0":
                        return
                    elif confirm == "y":
                        self.controller.stock_out(stock_id, qty)
                        print("Xuất kho thành công.")
                        return
                    elif confirm == "n":
                        print("Hủy xuất. Quay lại tìm kiếm kho.")
                        break
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")
                        continue
                break

    # 9. Xuất báo cáo CSV
    def xuat_csv(self, filename="report.csv"):
        output_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
        data = self.controller.get_all_stocks()
        if not data:
            print("Không có dữ liệu để xuất.")
            return
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID kho", "ID xe", "Dong xe", "Hang xe",
                "So luong ton kho", "Muc ton toi thieu", "Ngay nhap kho cuoi cung"
            ])
            for s in data:
                writer.writerow(s)
        print(f"Xuất báo cáo thành công ra {output_path}.")

