from django.db import models

class Mechanic(models.Model):
    mechanic_id = models.AutoField(primary_key=True)  # Explicit primary key
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    car_license_number = models.CharField(max_length=20)
    car_engine_number = models.CharField(max_length=20)
    appointment_date = models.DateField()

    # ForeignKey to mechanic_id of Mechanic table
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, db_column='mechanic_id')

    def __str__(self):
        return f"{self.client_name} - {self.appointment_date}"
class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password if secure

    def __str__(self):
        return self.username