from QUANLYCUAHANGXE.VehicleApp import VehicleApp

if __name__ == "__main__":
    app = VehicleApp()

    while True:
        print("\n--- QUẢN LÝ CỬA HÀNG XE ---")
        print("1. Xem danh sách xe")
        print("2. Thêm xe mới")
        print("0. Thoát")
        choice = input("Chọn: ")

        if choice == "1":
            app.hien_thi_ds_xe()
        elif choice == "2":
            app.them_xe_moi()
        elif choice == "0":
            print("Thoát ứng dụng!")
            break
        else:
            print("Lựa chọn không hợp lệ!")
