from app.vehicle_app import VehicleApp
from app.user_app import UserApp
from app.customer_app import CustomerApp
from app.order_app import OrderApp
from controller.user_controller import UserController

def dang_nhap_he_thong():
    user_controller = UserController()
    while True:
        username = input("Tên đăng nhập: ").strip()
        if username == "0":
            print("Hủy đăng nhập, quay lại menu chính!")
            return None

        password = input("Mật khẩu: ").strip()
        if password == "0":
            print("Hủy đăng nhập, quay lại menu chính!")
            return None

        if not username or not password:
            print("Tên đăng nhập và mật khẩu không được để trống!")
            continue

        user = user_controller.login(username, password)
        if user:
            return user[0]

def menu_quan_ly_xe(app: VehicleApp):
    while True:
        print("\n--- QUẢN LÝ DANH MỤC XE ---")
        print("1. Xem danh sách xe")
        print("2. Thêm xe mới")
        print("3. Cập nhật thông tin xe")
        print("4. Xóa xe")
        print("5. Xem chi tiết xe theo ID")
        print("6. Tìm kiếm theo hãng")
        print("7. Tìm kiếm theo năm sản xuất")
        print("8. Đếm số lượng xe")
        print("9. Xem xe mới nhất")
        print("10. Danh sách xe (phân trang)")
        print("11. Quay lại menu chính")
        choice = input("Chọn: ")
        if choice == "1":
            app.hien_thi_ds_xe()
        elif choice == "2":
            app.them_xe_moi()
        elif choice == "3":
            app.cap_nhat_xe()
        elif choice == "4":
            app.xoa_xe()
        elif choice == "5":
            app.xem_chi_tiet_xe()
        elif choice == "6":
            app.tim_theo_hang()
        elif choice == "7":
            app.tim_theo_nam()
        elif choice == "8":
            app.dem_so_luong_xe()
        elif choice == "9":
            app.xe_moi_nhat()
        elif choice == "10":
            app.ds_xe_phan_trang()
        elif choice == "11":
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")

def menu_quan_ly_user(app: UserApp):
    while True:
        print("\n--- QUẢN LÝ NGƯỜI DÙNG ---")
        print("1. Xem danh sách người dùng")
        print("2. Thêm người dùng mới")
        print("3. Cập nhật người dùng")
        print("4. Xóa người dùng")
        print("5. Xem chi tiết người dùng theo ID")
        print("6. Đăng nhập")
        print("7. Đổi mật khẩu")
        print("8. Tìm kiếm người dùng")
        print("9. Quay lại menu chính")
        choice = input("Chọn chức năng: ")
        if choice == "1":
            app.hien_thi_ds_user()
        elif choice == "2":
            app.them_user_moi()
        elif choice == "3":
            app.cap_nhat_user()
        elif choice == "4":
            app.xoa_user()
        elif choice == "5":
            app.xem_chi_tiet_user()
        elif choice == "6":
            app.dang_nhap()
        elif choice == "7":
            app.doi_mat_khau()
        elif choice == "8":
            app.tim_kiem_user()
        elif choice == "9":
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")

def menu_quan_ly_customer(app: CustomerApp):
    while True:
        print("\n--- QUẢN LÝ KHÁCH HÀNG ---")
        print("1. Xem danh sách khách hàng")
        print("2. Thêm khách hàng mới")
        print("3. Cập nhật khách hàng")
        print("4. Xóa khách hàng")
        print("5. Xem chi tiết khách hàng theo ID")
        print("6. Khóa/Mở khóa khách hàng")
        print("7. Tìm khách hàng theo tên/SĐT/Email")
        print("8. Thống kê")
        print("9. Khách hàng mới nhất")
        print("10. Quay lại menu chính")

        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            app.hien_thi_ds_customer()
        elif choice == "2":
            app.them_customer_moi()
        elif choice == "3":
            app.cap_nhat_customer()
        elif choice == "4":
            app.xoa_customer()
        elif choice == "5":
            app.xem_chi_tiet_customer()
        elif choice == "6":
            app.khoa_mo_khoa_customer()
        elif choice == "7":
            app.tim_customer()
        elif choice == "8":
            app.thong_ke_customer()
        elif choice == "9":
            app.khach_hang_moi_nhat()
        elif choice == "10":
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")

def menu_quan_ly_order(app: OrderApp, current_user_id):
    while True:
        print("\n--- QUẢN LÝ ĐƠN HÀNG ---")
        print("1. Xem danh sách đơn hàng")
        print("2. Xem chi tiết đơn hàng")
        print("3. Tạo đơn hàng mới")
        print("4. Cập nhật trạng thái đơn hàng")
        print("5. Tìm kiếm đơn hàng")
        print("6. Thống kê đơn hàng")
        print("7. In hóa đơn")
        print("8. Lịch sử cập nhật")
        print("9. Quay lại menu chính")
        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            app.hien_thi_ds_order()
        elif choice == "2":
            app.xem_chi_tiet_order()
        elif choice == "3":
            app.tao_order_moi(current_user_id)
        elif choice == "4":
            app.cap_nhat_trang_thai(current_user_id)
        elif choice == "5":
            app.tim_kiem_order()
        elif choice == "6":
            app.thong_ke_order()
        elif choice == "7":
            app.in_hoa_don()
        elif choice == "8":
            app.lich_su_cap_nhat()
        elif choice == "9":
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")


if __name__ == "__main__":
    vehicleApp = VehicleApp()
    userApp = UserApp()
    customerApp = CustomerApp()
    orderApp = OrderApp()
    current_user_id = None
    # hien_thi_thong_tin_he_thong()
    while True:
        print("=== MENU CHÍNH ===")
        print("1. Quản lý danh mục xe")
        print("2. Quản lý danh mục user")
        print("3. Quản lý danh mục khách hàng")
        print("4. Quản lý danh mục đơn hàng")
        print("0. Thoát")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            menu_quan_ly_xe(vehicleApp)
        elif choice == "2":
            menu_quan_ly_user(userApp)
        elif choice == "3":
            menu_quan_ly_customer(customerApp)
        elif choice == "4":
            if current_user_id:
                menu_quan_ly_order(orderApp, current_user_id)
            else:
                print("Vui lòng đăng nhập trước khi sử dụng chức năng quản lý đơn hàng!")
                current_user_id = dang_nhap_he_thong()
                if current_user_id:
                    menu_quan_ly_order(orderApp, current_user_id)
                    if current_user_id:
                        print("Đã đăng xuất!")
                        current_user_id = None
                    else:
                        current_user_id = dang_nhap_he_thong()
        elif choice == "0":
            print("Cảm ơn bạn đã sử dụng hệ thống! Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")