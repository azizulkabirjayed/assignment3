from django.contrib import admin
from .models import Mechanic, Appointment, AdminUser

# Admin configuration for Mechanic model
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('mechanic_id', 'name', 'phone')  # Fields to display as columns

# Admin configuration for Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'address', 'phone', 'car_license_number', 'car_engine_number', 'appointment_date', 'mechanic')  # Fields to display as columns

# Admin configuration for AdminUser model
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')  # Fields to display as columns

# Register models with their respective admin classes
admin.site.register(Mechanic, MechanicAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AdminUser, AdminUserAdmin)