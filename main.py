from app.vehicle_app import VehicleApp
from app.user_app import UserApp

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
        print("\n--- QUẢN LÝ USER ---")
        print("1. Xem danh sách User")
        print("2. Thêm User mới")
        print("3. Cập nhật User")
        print("4. Xóa User")
        print("5. Xem chi tiết User theo ID")
        print("6. Đăng nhập")
        print("7. Đổi mật khẩu")
        print("8. Tìm kiếm User")
        print("9. Khóa/Mở khóa tài khoản")
        print("10. Quay lại menu chính")
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
            app.khoa_mo_khoa_user()
        elif choice == "10":
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    vehicleApp = VehicleApp()
    userApp = UserApp()

    while True:
        print("\n=== MENU CHÍNH ===")
        print("1. Quản lý danh mục xe")
        print("2. Quản lý danh mục user")
        print("0. Thoát")
        choice = input("Chọn: ")

        if choice == "1":
            menu_quan_ly_xe(vehicleApp)
        elif choice == "2":
            menu_quan_ly_user(userApp)
        elif choice == "0":
            print("Thoát ứng dụng!")
            break
        else:
            print("Lựa chọn không hợp lệ!")