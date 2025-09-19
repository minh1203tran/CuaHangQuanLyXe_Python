from app.vehicle_app import VehicleApp
from app.user_app import UserApp
from app.customer_app import CustomerApp

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
            print("Lựa chọn không hợp lệ!")

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
        choice = input("Chọn: ")
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
            print("Lựa chọn không hợp lệ!")

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

        choice = input("Chọn: ").strip()
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
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    vehicleApp = VehicleApp()
    userApp = UserApp()
    customerApp = CustomerApp()

    while True:
        print("\n=== MENU CHÍNH ===")
        print("1. Quản lý danh mục xe")
        print("2. Quản lý danh mục user")
        print("3. Quản lý danh mục khách hàng")
        print("0. Thoát")
        choice = input("Chọn: ")

        if choice == "1":
            menu_quan_ly_xe(vehicleApp)
        elif choice == "2":
            menu_quan_ly_user(userApp)
        elif choice == "3":
            menu_quan_ly_customer(customerApp)
        elif choice == "0":
            print("Thoát ứng dụng!")
            break
        else:
            print("Lựa chọn không hợp lệ!")