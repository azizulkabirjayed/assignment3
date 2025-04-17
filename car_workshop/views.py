from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.utils.dateparse import parse_date
from datetime import date
from .models import Mechanic, Appointment, AdminUser




def index(request):
    if request.method == 'POST':
        client_name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        car_license = request.POST['car_license']
        car_engine = request.POST['car_engine']
        appointment_date = request.POST['date']
        mechanic_id = request.POST['mechanic']

        # Check if the car is already booked on this date
        exists = Appointment.objects.filter(
            car_license_number=car_license,
            appointment_date=appointment_date
        ).exists()
        if exists:
            messages.error(request, "You have already taken an appointment on this date.")
            mechanics = Mechanic.objects.all()
            return render(request, 'index.html', {'mechanics': mechanics})


        # Check if selected mechanic already has 4 appointments on this date
        mechanic_appointments_count = Appointment.objects.filter(
            mechanic_id=mechanic_id,
            appointment_date=appointment_date
        ).count()
        if mechanic_appointments_count >= 4:
            messages.error(request, "Selected mechanic already has 4 bookings on this date. Please choose another.")



        # Create appointment
        Appointment.objects.create(
            client_name=client_name,
            address=address,
            phone=phone,
            car_license_number=car_license,
            car_engine_number=car_engine,
            appointment_date=appointment_date,
            mechanic_id=mechanic_id
        )
        messages.success(request, "Your appointment has been booked successfully.")
        return redirect('appointment')  # redirect to appointment list or success page
    else:
        # Read selected date from the URL query parameter
        appointment_date = request.GET.get('date')
        
        if appointment_date:
            try:
                parsed_date = parse_date(appointment_date)
            except:
                parsed_date = date.today()
        else:
            parsed_date = date.today()

        # Get IDs of mechanics with 4 or more appointments on that date
        busy_mechanics = Appointment.objects.filter(
            appointment_date=parsed_date
        ).values('mechanic').annotate(count=Count('id')).filter(count__gte=4).values_list('mechanic', flat=True)

        # Get only available mechanics (less than 5 bookings)
        mechanics = Mechanic.objects.exclude(mechanic_id__in=busy_mechanics)

        # Send filtered mechanics and selected date to the template
        return render(request, 'index.html', {
            'mechanics': mechanics,
            'selected_date': parsed_date
        })






def appointment(request):
    return render(request, 'appointment.html')






def admin_view(request):

    appointments = Appointment.objects.select_related('mechanic').all()
    mechanics = Mechanic.objects.all()

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_date = request.POST.get('new_date')
        new_mechanic_id = request.POST.get('new_mechanic')

        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.appointment_date = new_date
        appointment.mechanic_id = new_mechanic_id
        appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('admin_view')  # Replace with your actual URL name

    return render(request, 'admin_view.html', {
        'appointments': appointments,
        'mechanics': mechanics
    })








def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin_user = AdminUser.objects.get(username=username)
            # If passwords are stored in plain text (not recommended), use this:
            if admin_user.password == password:
                # Save user info to session
                request.session['admin_username'] = admin_user.username
                return redirect('admin_view')
            else:
                messages.error(request, "Invalid password.")
        except AdminUser.DoesNotExist:
            messages.error(request, "Admin user not found.")
        return redirect('admin_login')

    # GET request → show login form
    return render(request, 'admin_login.html')






















