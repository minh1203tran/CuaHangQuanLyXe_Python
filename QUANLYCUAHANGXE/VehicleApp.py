from Controller.VehicleController import VehicleController

class VehicleApp:
    def __init__(self):
        self.controller = VehicleController()

    def hien_thi_ds_xe(self):
        self.controller.list_vehicles()

    def them_xe_moi(self):
        lp = input("Biển số: ")
        model = input("Mẫu xe: ")
        manu = input("Hãng: ")
        year = int(input("Năm SX: "))
        self.controller.add_vehicle(lp, model, manu, year)
