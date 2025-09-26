import csv
import os
from decimal import Decimal
from controller.payment_controller import PaymentController
from controller.order_controller import OrderController


class PaymentApp:
    def __init__(self):
        self.controller = PaymentController()
        self.order = OrderController()

    def get_input(self, prompt, default=None, allow_quit=True, to_upper=False, cast_func=None):
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
            return value

    # 1. Danh sách thanh toán
    def hien_thi_ds_payment(self):
        self.controller.list_payments()

    # 2. Thêm thanh toán
    def them_payment_moi(self):
        order_id = None
        while True:
            keyword = self.get_input("Nhập số điện thoại hoặc email khách hàng (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return
            results = self.order.search_orders(keyword)
            if not results:
                print("Không tìm thấy đơn hàng! Vui lòng nhập lại.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM ---")
            for row in results:
                print(f"ID đơn hàng: {row[0]} | Tên khách hàng: {row[1]} | "
                      f"Số điện thoại: {row[2]} | Trạng thái: {row[3]} | Ngày mua hàng: {row[4]}")
            while True:
                order_id_input = self.get_input("Chọn ID đơn hàng từ danh sách (0 để hủy): ", cast_func=int)
                if order_id_input == 0 or order_id_input is None:
                    return
                if order_id_input in [r[0] for r in results]:
                    if self.controller.has_payment(order_id_input):
                        print(f"Đơn hàng {order_id_input} đã thanh toán, vui lòng chọn đơn khác.")
                        continue
                    chosen_order = next(r for r in results if r[0] == order_id_input)
                    print("--- XÁC NHẬN ĐƠN HÀNG ---")
                    print(f"ID đơn hàng: {chosen_order[0]} | Tên khách hàng: {chosen_order[1]} | "
                          f"Số điện thoại: {chosen_order[2]} | Trạng thái: {chosen_order[3]} | Ngày mua hàng: {chosen_order[4]}")
                    while True:
                        confirm = self.get_input("Đơn hàng này đúng chưa? (y/n, 0 để hủy): ")
                        if confirm is None or confirm.strip() == "0":
                            return
                        if confirm.lower() == "y":
                            order_id = chosen_order[0]
                            break
                        elif confirm.lower() == "n":
                            print("Quay lại tìm kiếm đơn hàng.")
                            order_id = None
                            break
                        else:
                            print("Vui lòng nhập y/n hoặc 0 để hủy.")
                            continue
                    if order_id:
                        break
                    else:
                        break
                else:
                    print("ID đơn hàng không nằm trong danh sách! Vui lòng nhập lại.")
            if order_id:
                break
            else:
                continue
        order_total = self.order.get_order_total(order_id)
        print(f"Tổng tiền đơn hàng {order_id}: {order_total:,.0f} VND")
        paid_amount = 0
        payments_buffer = []
        while paid_amount < order_total:
            print(f"Đã thanh toán: {paid_amount:,.0f} VND | Còn lại: {order_total - paid_amount:,.0f} VND")
            amount = self.get_input("Nhập số tiền thanh toán (0 để hủy): ", cast_func=float)
            if amount is None or amount == 0:
                print("Hủy thao tác, các thanh toán tạm thời sẽ không được lưu.")
                return
            if amount <= 0:
                print("Số tiền phải lớn hơn 0! Vui lòng nhập lại.")
                continue
            while True:
                print("Chọn phương thức thanh toán:")
                print("1. Tiền mặt")
                print("2. Quẹt thẻ")
                print("3. Chuyển khoản")
                method_choice = self.get_input("Nhập số (1-3, 0 để hủy): ", cast_func=int)
                if method_choice is None or method_choice == 0:
                    print("Hủy thao tác, các thanh toán tạm thời sẽ không được lưu.")
                    return
                methods = {
                    1: "Tiền mặt",
                    2: "Quẹt thẻ",
                    3: "Chuyển khoản"
                }
                if method_choice not in methods:
                    print("Lựa chọn không hợp lệ! Vui lòng nhập 1, 2 hoặc 3.")
                    continue
                method = methods[method_choice]
                break
            transaction_id = self.get_input("Transaction ID: ")
            if transaction_id is None:
                print("Hủy thao tác, các thanh toán tạm thời sẽ không được lưu.")
                return
            while True:
                print("Chọn trạng thái thanh toán:")
                print("1. Thành công")
                print("2. Thất bại")
                status_choice = self.get_input("Nhập số (1-2, 0 để hủy): ", cast_func=int)
                if status_choice is None or status_choice == 0:
                    print("Hủy thao tác, các thanh toán tạm thời sẽ không được lưu.")
                    return
                statuses = {
                    1: "Thành công",
                    2: "Thất bại"
                }
                if status_choice not in statuses:
                    print("Lựa chọn không hợp lệ! Vui lòng nhập 1 hoặc 2.")
                    continue
                status = statuses[status_choice]
                if status == "Thất bại":
                    print("Giao dịch thất bại, vui lòng nhập lại thanh toán!")
                    break
                payments_buffer.append((order_id, amount, method, transaction_id, status))
                paid_amount += amount
                break
        for p in payments_buffer:
            self.controller.add_payment(*p)
        print(f"Thanh toán hoàn tất! Tổng đã thanh toán: {paid_amount:,.0f} VND")

    # 3. Cập nhật thanh toán
    def cap_nhat_payment(self):
        while True:
            keyword = self.get_input("Nhập tên khách hàng hoặc số điện thoại khách hàng (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return
            if not keyword.strip():
                print("Bạn phải nhập tên khách hàng hoặc số điện thoại để tìm kiếm!")
                continue
            payments = self.controller.search_payments(keyword)
            if not payments:
                print("Không tìm thấy thanh toán nào, vui lòng nhập lại.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM THANH TOÁN ---")
            for row in payments:
                print(
                    f"ID thanh toán: {row[0]} | ID đơn hàng: {row[1]} | "
                    f"Tên KH: {row[2]} | SĐT: {row[3]} | Số tiền: {row[4]:,.0f} | "
                    f"Phương thức: {row[5]} | Trạng thái: {row[7]} | Ngày: {row[8]}"
                )
            while True:
                payment_id = self.get_input("Chọn Payment ID từ danh sách (0 để hủy): ", cast_func=int)
                if payment_id is None or payment_id == 0:
                    return
                if payment_id not in [r[0] for r in payments]:
                    print("ID thanh toán không hợp lệ, vui lòng nhập lại.")
                    continue
                payment = self.controller.get_payment(payment_id)
                while True:
                    confirm = input(
                        f"Bạn có chắc chắn muốn cập nhật trạng thái cho Payment ID {payment_id}? (y/n, 0 để hủy): "
                    ).strip().lower()
                    if confirm == "y":
                        break
                    elif confirm == "n":
                        print("Hủy thao tác cập nhật, quay lại tìm kiếm thanh toán.")
                        break
                    elif confirm == "0":
                        print("Hủy thao tác cập nhật.")
                        return
                    else:
                        print("Vui lòng nhập y/n hoặc 0 để hủy.")
                if confirm != "y":
                    break
                self.controller.show_payment_detail(payment)
                while True:
                    print("Chọn trạng thái thanh toán mới (0 để hủy, Enter giữ nguyên):")
                    print("1. Thành công")
                    print("2. Thất bại")
                    status_input = input(f"Nhập số (hiện tại: {payment[7]}): ").strip()
                    if not status_input:
                        status = payment[7]
                        break
                    if status_input == "0":
                        print("Hủy thao tác cập nhật.")
                        return
                    try:
                        status_choice = int(status_input)
                    except ValueError:
                        print("Vui lòng nhập số hợp lệ!")
                        continue
                    statuses = {1: "Thành công", 2: "Thất bại"}
                    if status_choice in statuses:
                        status = statuses[status_choice]
                        break
                    else:
                        print("Lựa chọn không hợp lệ! Vui lòng nhập 1 hoặc 2.")
                old_status = payment[7]
                self.controller.update_payment(payment_id, payment[4], payment[5], status)
                if old_status != status:
                    print(f"Trạng thái thanh toán đã thay đổi từ '{old_status}' sang '{status}'.")
                else:
                    print(f"Trạng thái thanh toán giữ nguyên: '{status}'.")
                return

    # 4. Xóa thanh toán
    def xoa_payment(self):
        while True:
            keyword = self.get_input("Nhập tên khách hàng hoặc số điện thoại để tìm kiếm ID (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return
            if not keyword.strip():
                print("Bạn phải nhập thông tin để tìm kiếm!")
                continue
            payments = self.controller.search_payments(keyword)
            payments = [p for p in payments if p[7] == "Thất bại"]
            if not payments:
                print("Không tìm thấy thanh toán nào có trạng thái 'Thất bại', vui lòng nhập lại.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM THANH TOÁN ---")
            for row in payments:
                print(
                    f"ID thanh toán: {row[0]} | ID đơn hàng: {row[1]} | "
                    f"Tên khách hàng: {row[2]} | số điện thoại: {row[3]} | Số tiền: {row[4]:,.0f} | "
                    f"Phương thức: {row[5]} | Trạng thái: {row[7]} | Ngày: {row[8]}"
                )
            while True:
                payment_id = self.get_input("Chọn ID thanh toán cần xóa (0 để hủy): ", cast_func=int)
                if payment_id is None or payment_id == 0:
                    print("Hủy thao tác xóa.")
                    return
                if payment_id not in [r[0] for r in payments]:
                    print("ID thanh toán không hợp lệ hoặc không phải trạng thái thất bại, vui lòng nhập lại.")
                    continue
                payment = self.controller.get_payment(payment_id)
                if not payment:
                    print(f"ID thanh toán {payment_id} không tồn tại.")
                    continue
                self.controller.show_payment_detail(payment)
                confirm = self.get_input("Bạn có chắc chắn muốn xóa? (y/n, 0 để hủy): ", to_upper=True)
                if confirm is None:
                    continue
                confirm = confirm.strip().upper()
                if confirm == "Y":
                    self.controller.delete_payment(payment_id)
                    print("Xóa thành công.")
                    return
                elif confirm == "N":
                    print("Hủy thao tác xóa, quay lại tìm kiếm thanh toán.")
                    break
                elif confirm == "0":
                    print("Hủy thao tác xóa.")
                    return
                else:
                    print("Vui lòng nhập y/n hoặc 0 để hủy.")

    # 5. Tìm kiếm thanh toán
    def tim_kiem_payment(self):
        while True:
            keyword = self.get_input("Nhập tên khách hàng hoặc số điện thoại để tìm kiếm Payment (0 để hủy): ")
            if keyword is None or keyword.strip() == "0":
                return
            if not keyword.strip():
                print("Bạn phải nhập thông tin để tìm kiếm!")
                continue
            payments = self.controller.search_payments(keyword)
            if not payments:
                print("Không tìm thấy thanh toán nào, vui lòng nhập lại.")
                continue
            print("--- KẾT QUẢ TÌM KIẾM THANH TOÁN ---")
            for row in payments:
                print(
                    f"ID thanh toán: {row[0]} | ID đơn hàng: {row[1]} | "
                    f"Tên khách hàng: {row[2]} | số điện thoại: {row[3]} | "
                    f"Số tiền: {row[4]:,.0f} | Phương thức: {row[5]} | "
                    f"Trạng thái: {row[7]} | Ngày: {row[8]}"
                )
            break

    # 6. Xuất báo cáo CSV
    def xuat_csv(self, filename="payments_report.csv"):
        output_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
        data = self.controller.get_all_payments()
        if not data:
            print("Không có dữ liệu để xuất.")
            return
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "PAYMENT_ID", "ORDER_ID", "AMOUNT", "PAYMENT_DATE",
                "PAYMENT_METHOD", "TRANSACTION_ID", "STATUS"
            ])
            for row in data:
                writer.writerow(row)
        print(f"Xuất báo cáo thành công ra {output_path}")

    # 7. Lọc theo trạng thái
    def filter_by_status(self):
        while True:
            print("\n--- LỌC THEO TRẠNG THÁI ---")
            print("1. Thành công")
            print("2. Thất bại")
            print("0. Quay lại")
            choice = self.get_input("Chọn trạng thái: ", cast_func=int)
            if choice is None:
                return
            if choice == 0:
                print("Thoát chức năng lọc.")
                return
            elif choice == 1:
                status = "Thành công"
            elif choice == 2:
                status = "Thất bại"
            else:
                print("Lựa chọn không hợp lệ, quay lại menu chính.")
                continue
            payments = self.controller.filter_status(status)
            if not payments:
                print(f"Không tìm thấy thanh toán nào với trạng thái: {status}")
                return
            print(f"--- DANH SÁCH THANH TOÁN ({status}) ---")
            for row in payments:
                print(
                    f"ID thanh toán: {row[0]} | ID đơn hàng: {row[1]} | "
                    f"Số tiền: {row[2]:,.0f} | Ngày: {row[3]} | "
                    f"Phương thức: {row[4]} | Transaction: {row[5]} | "
                    f"Trạng thái: {row[6]}"
                )
            return

    # 8. Thống kê thanh toán
    def stats(self):
        stats = self.controller.payment_stats()
        print("\n--- THỐNG KÊ THANH TOÁN ---")
        if not stats:
            print("⚠️ Không có dữ liệu thống kê.")
            return

        for row in stats:
            # row là tuple (STATUS, COUNT, TOTAL)
            status = row[0]
            count = row[1]
            total = row[2]
            print(f"Trạng thái: {status} | Số lượng: {count} | Tổng số tiền: {total:,.0f}")

