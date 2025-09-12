from MSSQLServer.MSSQLServer import Database

class VehicleModel:
    def __init__(self):
        self.conn = Database.get_instance()

    def get_all(self):
        sql = "SELECT VEHICLESID, LICENSEPLATE, MODEL, MANUFACTURER, YEAR FROM Vehicles"
        return self.conn.query(sql)

    def add_vehicle(self, license_plate, model, manufacturer, year):
        sql = "INSERT INTO Vehicles (LICENSEPLATE, MODEL, MANUFACTURER, YEAR) VALUES (?, ?, ?, ?)"
        return self.conn.query(sql, (license_plate, model, manufacturer, year))