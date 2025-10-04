from datetime import datetime
from model.service_model import ServiceModel
from view.service_view import ServiceView

class ServiceController:
    def __init__(self):
        self.model = ServiceModel()
        self.view = ServiceView()

    def get_and_show_customers(self, keyword=None):
        customers = self.model.get_customers_for_selection(keyword)
        self.view.show_customer_selection(customers)
        return customers

    # 1. Danh sách dịch vụ
    def list_services(self):
        services = self.model.get_all()
        self.view.show_list(services)
        return services

    # 2. Thêm dịch vụ mới
    def add_service(self, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status):
        return self.model.insert(customer_id, vehicle_id, service_type, service_date, cost, technician_id, status)

    def get_and_show_vehicles(self, keyword=None):
        vehicles = self.model.get_vehicles_for_selection(keyword)
        self.view.show_vehicle_selection(vehicles)
        return vehicles

    def get_and_show_technicians(self, keyword=None):
        technicians = self.model.get_technicians_for_selection(keyword)
        self.view.show_technician_selection(technicians)
        return technicians

    # 3. Cập nhật dịch vụ
    def update_service(self, service_id, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status):
        return self.model.update(service_id, customer_id, vehicle_id, service_type, service_date, cost, technician_id, status)

    def show_service_detail(self, service_id):
        service = self.model.get_by_id(service_id)
        if service:
            self.view.show_detail(service)
        return service

    # 4. Xóa dịch vụ
    def delete_service(self, service_id):
        return self.model.delete(service_id)

    def get_and_show_service_detail(self, service_id):
        service = self.model.get_by_id(service_id)
        self.view.show_detail(service)
        return service

    def show_service_list(self, services):
        self.view.show_list(services)

    def get_service(self, service_id):
        return self.model.get_by_id(service_id)

    # 5. Tìm kiếm dịch vụ
    def search_services(self, keyword):
        return self.model.search(keyword)

    # 6. Xuất báo cáo CSV
    def get_all_services(self):
        return self.model.get_all()

    # 7. Lọc theo trạng thái
    def filter_services_by_status(self, status):
        return self.model.filter_by_status(status)

    # 8. Lọc theo ngày
    def filter_services_by_date(self, start_date, end_date):
        return self.model.filter_by_date(start_date, end_date)

    # 9. Thống kê dịch vụ
    def get_service_stats_by_status(self):
        stats = self.model.get_service_stats_by_status()
        self.view.show_stats(stats)
        return stats

    def get_service_stats_by_type(self):
        stats = self.model.get_service_stats_by_type()
        self.view.show_total_cost_by_service_type(stats)
        return stats