from datetime import datetime
from controller.order_controller import OrderController
from controller.customer_controller import CustomerController
from controller.user_controller import UserController
from controller.vehicle_controller import VehicleController

class OrderApp:
    def __init__(self):
        self.controller = OrderController()
        self.customer = CustomerController()
        self.user = UserController()
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

    # 1. Xem danh sách đơn hàng
    def hien_thi_ds_order(self):
        self.controller.list_orders()

    # 2. Xem chi tiết đơn hàng
    def xem_chi_tiet_order(self):
        self.controller.list_orders()
        while True:
            order_id = self.get_input("Nhập ID đơn hàng (0 để hủy): ", cast_func=int)
            if order_id is None:
                return
            order = self.controller.view_order(order_id)
            if order:
                break

    # 3. Tạo đơn hàng mới
    def tao_order_moi(self, current_user_id):
        while True:
            keyword = self.get_input("Nhập tên/SĐT/Email khách hàng (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return
            if not keyword.strip():
                print("Bạn phải nhập từ khóa tìm kiếm! Vui lòng nhập lại.")
                continue
            results = self.customer.search_customer(keyword)
            if not results:
                print("Không tìm thấy khách hàng! Vui lòng nhập lại.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM ---")
            for row in results:
                print(f"ID: {row[0]} | Họ tên: {row[2]} | Email: {row[3]} | Phone: {row[4]}")
            while True:
                customer_id = self.get_input("Chọn ID khách hàng từ danh sách (0 để hủy): ", cast_func=int)
                if customer_id == 0 or customer_id is None:
                    return
                if customer_id in [r[0] for r in results]:
                    chosen_customer = next(r for r in results if r[0] == customer_id)
                    print("--- XÁC NHẬN KHÁCH HÀNG ---")
                    print(f"ID: {chosen_customer[0]} | Họ tên: {chosen_customer[2]} | "
                          f"Email: {chosen_customer[3]} | Phone: {chosen_customer[4]}")
                    while True:
                        confirm = self.get_input("Khách hàng này đúng chưa? (y/n, 0 để hủy): ")
                        if confirm is None or confirm.strip() == "0":
                            return
                        if confirm.lower() == "y":
                            break
                        elif confirm.lower() == "n":
                            print("Quay lại tìm kiếm khách hàng.")
                            chosen_customer = None
                            break
                        else:
                            print("Vui lòng nhập y/n hoặc 0 để hủy.")
                            continue
                    if confirm and confirm.lower() == "y":
                        break
                    elif confirm.lower() == "n":
                        break
                else:
                    print("ID khách hàng không nằm trong danh sách bạn tìm! Vui lòng nhập lại.")
                    continue
            if chosen_customer:
                break
        # while True:
        #     keyword = self.get_input("Nhập tên nhân viên hoặc username (0 để hủy): ")
        #     if keyword is None or keyword.strip() == "0":
        #         return
        #     if not keyword.strip():
        #         print("Bạn phải nhập từ khóa tìm kiếm! Vui lòng nhập lại.")
        #         continue
        #     users = self.user.find_user(keyword)
        #     if not users:
        #         print("Không tìm thấy nhân viên! Vui lòng nhập lại.")
        #         continue
        #     print("--- DANH SÁCH NHÂN VIÊN ---")
        #     for u in users:
        #         print(f"ID: {u[0]} | Username: {u[1]} | Họ tên: {u[2]}")
        #     chosen_user = None
        #     while True:
        #         user_id = self.get_input("Chọn ID nhân viên từ danh sách (0 để hủy): ", cast_func=int)
        #         if user_id == 0 or user_id is None:
        #             return
        #         if user_id in [u[0] for u in users]:
        #             chosen_user = next(u for u in users if u[0] == user_id)
        #             print("--- XÁC NHẬN NHÂN VIÊN ---")
        #             print(f"ID: {chosen_user[0]} | Username: {chosen_user[1]} | Họ tên: {chosen_user[2]}")
        #             while True:
        #                 confirm = self.get_input("Nhân viên này đúng chưa? (y/n, 0 để hủy): ")
        #                 if confirm is None or confirm.strip() == "0":
        #                     return
        #                 if confirm.lower() == "y":
        #                     break
        #                 elif confirm.lower() == "n":
        #                     print("Quay lại tìm kiếm nhân viên.")
        #                     chosen_user = None
        #                     break
        #                 else:
        #                     print("Vui lòng nhập y/n hoặc 0 để hủy.")
        #                     continue
        #             if confirm.lower() == "y":
        #                 break
        #             elif confirm.lower() == "n":
        #                 break
        #         else:
        #             print("ID nhân viên không nằm trong danh sách bạn tìm! Vui lòng nhập lại.")
        #             continue
        #     if chosen_user:
        #         break
        user_id = current_user_id
        payment_options = {1: "Tiền mặt", 2: "Thẻ ngân hàng", 3: "Trả góp"}
        while True:
            print("Chọn hình thức thanh toán:")
            for k, v in payment_options.items():
                print(f"{k}. {v}")
            choice = self.get_input("Nhập số (1 - 3, 0 để hủy): ", cast_func=int)
            if choice is None or choice == 0:
                return
            if choice in payment_options:
                payment_method = payment_options[choice]
                break
            else:
                print("Chỉ chọn các số 1 - 3 hoặc 0 để hủy thao tác! Vui lòng nhập lại.")
        while True:
            delivery_address = self.get_input("Địa chỉ giao hàng (bắt buộc): ")
            if delivery_address and delivery_address.strip() != "":
                break
            else:
                print("Địa chỉ giao hàng không được để trống! Vui lòng nhập lại.")
        note = self.get_input("Ghi chú: ")
        order_items = []
        while True:
            keyword = self.get_input("Nhập hãng xe (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
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
            chosen_vehicle = None
            while True:
                vehicle_id = self.get_input("Chọn ID xe từ danh sách (0 để hủy): ", cast_func=int)
                if vehicle_id == 0 or vehicle_id is None:
                    return
                if vehicle_id in [v[0] for v in vehicles]:
                    chosen_vehicle = next(v for v in vehicles if v[0] == vehicle_id)
                    print("--- XÁC NHẬN XE ---")
                    print(f"ID: {chosen_vehicle[0]} | Biển số: {chosen_vehicle[1]} | "
                          f"Dòng xe: {chosen_vehicle[2]} | Hãng: {chosen_vehicle[3]} | Giá: {chosen_vehicle[6]}")
                    while True:
                        confirm = self.get_input("Xe này đúng chưa? (y/n, 0 để hủy): ")
                        if confirm is None or confirm.strip() == "0":
                            return
                        if confirm.lower() == "y":
                            break
                        elif confirm.lower() == "n":
                            print("Quay lại tìm kiếm xe.")
                            chosen_vehicle = None
                            break
                        else:
                            print("Vui lòng nhập y/n hoặc 0 để hủy.")
                            continue
                    if confirm.lower() == "y":
                        break
                    elif confirm.lower() == "n":
                        break
                else:
                    print("ID xe không nằm trong danh sách bạn tìm! Vui lòng nhập lại.")
                    continue
            if chosen_vehicle:
                quantity = self.get_input("Số lượng (Enter = 1): ", default=1, cast_func=int)
                try:
                    default_price = float(chosen_vehicle[6]) if chosen_vehicle[6] is not None else 0.0
                except (ValueError, TypeError):
                    default_price = 0.0
                unit_price = self.get_input("Đơn giá (Enter để lấy giá gốc): ",
                                            default=default_price, cast_func=float)
                order_items.append({
                    'vehicle_id': chosen_vehicle[0],
                    'quantity': quantity,
                    'unit_price': unit_price
                })
                done = False
                while True:
                    more = self.get_input("Bạn có muốn thêm xe khác không? (y/n, 0 để hủy): ")
                    if more is None or more.strip() == "0":
                        return
                    if more.lower() in ("y", "n"):
                        if more.lower() == "n":
                            done = True
                        break
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")
                if done:
                    break
        print("===== XÁC NHẬN ĐƠN HÀNG =====")
        print(f"Khách hàng: {chosen_customer[2]} ({chosen_customer[3]} | {chosen_customer[4]})")
        # print(f"Nhân viên: {chosen_user[2]} (Username: {chosen_user[1]})")
        print(f"Nhân viên: {user_id}")
        print(f"Thanh toán: {payment_method}")
        print(f"Địa chỉ: {delivery_address}")
        print(f"Ghi chú: {note}")
        print("Chi tiết đơn hàng:")
        for item in order_items:
            print(f"- ID xe: {item['vehicle_id']} | Số lượng: {item['quantity']} | Đơn giá: {item['unit_price']}")
        while True:
            confirm = self.get_input("Bạn có muốn lưu đơn hàng này? (y/n, 0 để hủy): ")
            if confirm is None or confirm.strip() == "0":
                return
            if confirm.lower() == "y":
                self.controller.add_order(customer_id, user_id, payment_method, delivery_address, note, order_items)
                break
            elif confirm.lower() == "n":
                print("Đơn hàng KHÔNG được lưu.")
                break
            else:
                print("Vui lòng nhập y/n hoặc 0 để hủy.")

    # 4. Cập nhật trạng thái đơn hàng
    def cap_nhat_trang_thai(self, current_user_id):
        print("=== CẬP NHẬT TRẠNG THÁI ĐƠN HÀNG ===")
        while True:
            keyword = input("Nhập tên KH hoặc số điện thoại (0 để thoát): ").strip()
            if keyword == "0":
                print("Hủy thao tác, quay lại menu chính!")
                return
            if keyword == "":
                print("Bạn phải nhập tên KH hoặc số điện thoại!")
                continue
            orders = self.controller.search_orders(keyword=keyword, limit=20)
            if not orders:
                print("Không tìm thấy đơn hàng nào! Vui lòng thử lại.")
                continue
            print("Danh sách đơn hàng tìm được:")
            for o in orders:
                print(f"ID: {o[0]}, Khách: {o[1]}, SĐT: {o[2]}, Trạng thái: {o[3]}, Ngày: {o[4]}")
            while True:
                try:
                    order_id_input = input("Nhập ID đơn hàng cần cập nhật (0 để thoát): ").strip()
                    if order_id_input == "0":
                        print("Hủy thao tác, quay lại menu chính!")
                        return
                    order_id = int(order_id_input)
                except ValueError:
                    print("Vui lòng nhập thông tin theo danh sách đã in ra!")
                    continue
                if order_id not in [o[0] for o in orders]:
                    print("ID không nằm trong danh sách kết quả tìm kiếm! Vui lòng chọn lại.")
                    continue
                selected_order = next(o for o in orders if o[0] == order_id)
                print(f"Đơn hàng bạn chọn: ID: {selected_order[0]}, Tên khách: {selected_order[1]}, "
                      f"SĐT: {selected_order[2]}, Trạng thái hiện tại: {selected_order[3]}")
                break
            status_options = ["Chưa duyệt", "Đã xác nhận", "Đã trả", "Đã giao hàng", "Đã hủy"]
            print("Chọn trạng thái mới:")
            for i, s in enumerate(status_options, start=1):
                print(f"{i}. {s}")
            while True:
                try:
                    choice_input = input("Nhập số (1-5, 0 để hủy): ").strip()
                    if choice_input == "0":
                        print("Hủy thao tác cập nhật trạng thái!")
                        return
                    choice = int(choice_input)
                except ValueError:
                    print("Vui lòng nhập số hợp lệ!")
                    continue
                if 1 <= choice <= len(status_options):
                    new_status = status_options[choice - 1]
                    break
                else:
                    print("Vui lòng chọn số trong khoảng 1-5!")
            old_status, _ = self.controller.update_order_status_and_get_old(order_id, new_status)
            self.controller.add_order_history(order_id, current_user_id, "Cập nhật trạng thái", old_status, new_status)
            print(f"Đã cập nhật trạng thái đơn hàng {order_id} từ '{old_status}' sang '{new_status}'.")
            return

    # 5. Tìm kiếm đơn hàng
    def tim_kiem_order(self):
        while True:
            keyword = self.get_input(
                prompt="Nhập tên khách hàng hoặc số điện thoại (0 để thoát): ",
                allow_quit=True,
                validator=lambda x: bool(x.strip())
            )
            if keyword is None:
                return
            orders = self.controller.search_orders(keyword=keyword, limit=20)
            if not orders:
                print("Không tìm thấy đơn hàng nào! Vui lòng thử lại.")
                continue
            print(f"Tìm thấy {len(orders)} đơn hàng:")
            for order in orders:
                order_id, customer_name, phone, status, date = order
                print(f"ID: {order_id} | Khách: {customer_name} | SĐT: {phone} | Trạng thái: {status} | Ngày: {date}")
            return

    # 6. Thống kê đơn hàng
    def thong_ke_order(self):
        while True:
            print("\n--- THỐNG KÊ ĐƠN HÀNG ---")
            print("1. Theo trạng thái")
            print("2. Theo ngày")
            print("3. Theo tháng")
            print("4. Theo khoảng thời gian")
            choice = self.get_input("Chọn loại thống kê (0 hủy thao tác): ", cast_func=int)
            if choice is None or choice == 0:
                return
            if choice == 1:
                statuses = ["Chưa duyệt", "Đã xác nhận", "Đang giao hàng", "Đã giao hàng", "Đã hủy"]
                for status in statuses:
                    orders = self.controller.get_orders_by_status(status)
                    print(f"\nTrạng thái của đơn hàng: {status}")
                    if not orders:
                        print("Trạng thái này không có đơn hàng nào!")
                        continue
                    print("Danh sách đơn hàng:")
                    for o in orders:
                        print(f"ID: {o[0]}, Khách: {o[1]}, SĐT: {o[2]}, Tổng: {o[3]}, Trạng thái: {o[4]}, Ngày: {o[5]}")
                    print(f"Tổng số đơn {status}: {len(orders)}")
            elif choice in [2, 3]:
                period = 'month' if choice == 3 else 'day'
                stats = self.controller.get_sales_statistics(period)
                print(f"\n--- THỐNG KÊ THEO {'THÁNG' if period == 'month' else 'NGÀY'} ---")
                for stat in stats:
                    if period == 'month':
                        print(f"{stat[0]}-{stat[1]:02d}: {stat[2]} đơn, Doanh thu: {stat[3]:,}")
                    else:
                        print(f"{stat[0]}: {stat[1]} đơn, Doanh thu: {stat[2]:,}")
            elif choice == 4:
                while True:
                    start_date_str = self.get_input("Ngày bắt đầu (YYYY-MM-DD) (0 để quay lại): ", allow_quit=True)
                    if start_date_str is None:
                        return
                    end_date_str = self.get_input("Ngày kết thúc (YYYY-MM-DD) (0 để quay lại): ", allow_quit=True)
                    if end_date_str is None:
                        return
                    try:
                        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        print("Ngày không hợp lệ! Vui lòng nhập lại theo định dạng YYYY-MM-DD.")
                        continue
                    if start_date > end_date:
                        print("Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc!")
                        continue
                    orders = self.controller.get_orders_by_date_range(str(start_date), str(end_date))
                    if not orders:
                        print("Không có đơn hàng trong khoảng thời gian này!")
                        continue
                    print("\nDanh sách đơn hàng:")
                    for o in orders:
                        print(f"ID: {o[0]}, Khách: {o[1]}, SĐT: {o[2]}, Tổng: {o[3]}, Trạng thái: {o[4]}, Ngày: {o[5]}")
                    total_revenue = sum(order[3] for order in orders if order[3])
                    print(f"Tổng số đơn: {len(orders)}, Tổng doanh thu: {total_revenue:,}\n")
                    break

    # 7. In hóa đơn
    def in_hoa_don(self):
        print("=== IN HÓA ĐƠN ĐƠN HÀNG ===")
        while True:
            keyword = self.get_input(
                prompt="Nhập tên KH hoặc số điện thoại (0 để thoát): ",
                allow_quit=True,
                validator=lambda x: bool(x.strip())
            )
            if keyword is None:
                return
            orders = self.controller.search_orders(keyword=keyword, limit=20)
            if not orders:
                print("Không tìm thấy đơn hàng nào! Vui lòng thử lại.")
                continue
            print("Danh sách đơn hàng tìm được:")
            for o in orders:
                print(f"ID: {o[0]}, Khách: {o[1]}, SĐT: {o[2]}, Trạng thái: {o[3]}, Ngày: {o[4]}")
            while True:
                try:
                    order_id = self.get_input(
                        "Nhập ID đơn hàng cần in (0 để thoát): ",
                        cast_func=int,
                        allow_quit=True
                    )
                except ValueError:
                    print("Vui lòng nhập ID hợp lệ!")
                    continue
                if order_id is None:
                    return
                if order_id not in [o[0] for o in orders]:
                    print("ID không nằm trong danh sách kết quả tìm kiếm! Vui lòng chọn lại.")
                    continue
                break
            order, details = self.controller.print_invoice(order_id)
            if not order or not details:
                print("Không tìm thấy chi tiết đơn hàng!")
                return
            print("" + "=" * 60)
            print("HÓA ĐƠN BÁN HÀNG".center(60))
            print("=" * 60)
            print(f"Mã đơn: {order[0]}".ljust(30) + f"Ngày: {order[5]}")
            print(f"Khách hàng: {order[2]}")
            print(f"Nhân viên: {order[4]}")
            print(f"Địa chỉ: {order[9]}")
            print(f"Phương thức: {order[8]}".ljust(30) + f"Trạng thái: {order[7]}")
            print("=" * 60)
            print("SẢN PHẨM".ljust(25) + "SL".center(5) + "ĐƠN GIÁ".rjust(15) + "THÀNH TIỀN".rjust(15))
            print("=" * 60)
            for d in details:
                product_name = f"{d[3]} {d[2]}"
                if len(product_name) > 25:
                    product_name = product_name[:22] + "..."
                print(
                    f"{product_name.ljust(25)}{str(d[3]).center(5)}{str(f'{d[4]:,}').rjust(15)}{str(f'{d[5]:,}').rjust(15)}")
            print("=" * 60)
            print(f"TỔNG CỘNG: {order[6]:,}".rjust(60))
            print("=" * 60)
            return

    # 8. Lịch sử cập nhật
    def lich_su_cap_nhat(self):
        print("=== LỊCH SỬ CẬP NHẬT ĐƠN HÀNG ===")
        while True:
            keyword = self.get_input(
                prompt="Nhập tên KH hoặc số điện thoại (0 để hủy chức năng): ",
                allow_quit=True,
                validator=lambda x: bool(x.strip())
            )
            if keyword is None:
                return
            orders = self.controller.search_orders(keyword=keyword, limit=20)
            if not orders:
                print("Không tìm thấy đơn hàng nào! Vui lòng thử lại.")
                continue
            print("Danh sách đơn hàng tìm được:")
            for o in orders:
                print(f"ID: {o[0]}, Khách: {o[1]}, SĐT: {o[2]}, Trạng thái: {o[3]}, Ngày: {o[4]}")
            while True:
                order_id = self.get_input(
                    "Nhập ID đơn hàng cần xem lịch sử (0 để thoát): ",
                    cast_func=int,
                    allow_quit=True
                )
                if order_id is None:
                    return
                if order_id not in [o[0] for o in orders]:
                    print("ID không nằm trong danh sách kết quả tìm kiếm! Vui lòng chọn lại.")
                    continue
                history = self.controller.get_order_history(order_id)
                if not history:
                    print(f"Không có lịch sử cập nhật cho đơn hàng {order_id}")
                    continue
                break
            print(f"\n--- LỊCH SỬ CẬP NHẬT ĐƠN HÀNG {order_id} ---")
            for h in history:
                print(f"{h[4]} - {h[0]} {h[1]} từ '{h[2]}' thành '{h[3]}'")
            return
