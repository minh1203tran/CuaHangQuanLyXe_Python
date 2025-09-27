from datetime import datetime
from model.appointment_model import AppointmentModel
from view.appointment_view import AppointmentView

class AppointmentController:
    def __init__(self):
        self.model = AppointmentModel()
        self.view = AppointmentView()

    def get_and_show_customers(self, keyword=None):
        customers = self.model.get_customers_for_selection(keyword)
        self.view.show_customer_selection(customers)
        return customers

    # 1. Danh sách lịch hẹn
    def list_appointments(self):
        appointments = self.model.get_all()
        self.view.show_list(appointments)
        return appointments

    # 2. Thêm lịch hẹn mới
    def add_appointment(self, customer_id, purpose, appointment_date, appointment_time, status):
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        return self.model.insert(customer_id, purpose, appointment_datetime, status)

    # 3. Cập nhật lịch hẹn
    def update_appointment(self, appointment_id, customer_id, purpose, appointment_date, appointment_time, status):
        # gộp date + time thành datetime
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        return self.model.update(appointment_id, customer_id, purpose, appointment_datetime, status)

    def show_appointments(self, appointments):
        self.view.show_list(appointments)
        return appointments

    def get_and_show_appointment_detail(self, appointment_id):
        appointment = self.model.get_by_id(appointment_id)
        self.view.show_detail(appointment)
        return appointment

    def get_appointment(self, appointment_id):
        return self.model.get_by_id(appointment_id)

    # Cập nhật trạng thái lịch hẹn
    # def update_appointment_status(self, appointment_id, status):
    #     return self.model.update_status(appointment_id, status)

    # 4. Xóa lịch hẹn
    def delete_appointment(self, appointment_id):
        return self.model.delete(appointment_id)

    # 5. Tìm kiếm lịch hẹn
    def search_appointments(self, keyword):
        return self.model.search(keyword)

    # 7. Lọc theo trạng thái
    def filter_appointments_by_status(self, status):
        return self.model.filter_by_status(status)

    # 8. Lọc theo ngày
    def filter_appointments_by_date(self, start_date, end_date):
        return self.model.filter_by_date(start_date, end_date)

    # 9. Thống kê lịch hẹn
    def get_appointment_stats(self):
        return self.model.stats_by_status()