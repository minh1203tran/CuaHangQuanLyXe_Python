from Model.VehicleModel import VehicleModel
from View.VehicleView import VehicleView

class VehicleController:
    def __init__(self):
        self.model = VehicleModel()
        self.view = VehicleView()

    def list_vehicles(self):
        data = self.model.get_all()
        self.view.show_list(data)

    def add_vehicle(self, license_plate, model, manufacturer, year):
        self.model.add_vehicle(license_plate, model, manufacturer, year)
        self.view.show_message("Đã thêm xe thành công!")
