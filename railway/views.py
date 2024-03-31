from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime


def home(request) : 
    return render(request,'index.html')

def login_first(request) : 
    return render(request,'login-register.html')

def register_user(request):
    flag = False
    if request.method == 'POST' :
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        user_name = request.POST['userName']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email)
        mobile_no = request.POST['mobile']
        gender = request.POST['gender']
        dob = request.POST['dob']
        register = Register.objects.create(
            user=user,
            mobile=mobile_no,
            gender=gender,
            dob =dob
        )

        user_profile = UserProfile.objects.create(user=user)
        
        flag = True
    
    data = {'passanger':False,'staff':False,'invalid_user':False,'flag':flag}
    return render(request,'login-register.html',data)

def login_user(request):
    invalid_user = False
    staff = False
    passanger = False
    if request.method == 'POST' :
        uname = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=uname,password=password)
            if user is None : 
                invalid_user = True
        except:
            # print("inside the except")
            invalid_user = True
        try:
            if user.is_staff:
                login(request,user)
                staff = True
            elif user:
                login(request,user)
                passanger=True
        except Exception as e:
            # Log the exception for debugging
            print(f"An exception occurred during authentication: {e}")
            invalid_user=True
    data = {'passanger':passanger,'staff':staff,'invalid_user':invalid_user,'flag':False,'u':user}

    return render(request,'login-register.html',data)

def logout_user(request) : 
    logout(request)
    return redirect("/")

@login_required
def user_home(request) :
    return render(request,'user_home.html')

def profile(request):
    user_info, created = Register.objects.get_or_create(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    data = {"user_info":user_info,"user_profile":user_profile}
    return render(request,"user_profile.html",data)

def edit_profile(request):
    register = Register.objects.get(user=request.user)
    data = {"register":register}
    if request.method == "POST" : 
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        photo = request.FILES.get('profile_photo')
        dob = request.POST['dob']
        gender = request.POST['gender']
        # Parse the date string into a datetime object
        dob_date = datetime.strptime(dob, "%B %d, %Y")

        # Format the datetime object into "YYYY-MM-DD" format
        dob_formatted = dob_date.strftime("%Y-%m-%d")
        curr_user = request.user
        curr_user.first_name= first_name
        curr_user.last_name = last_name
        curr_user.email = email
        #update the information of current user
        curr_user.save()

        register = Register.objects.get(user = request.user)
        register.mobile = mobile
        register.dob = dob_date
        register.gender = gender
        register.save()
        #set the photo of user
        testing, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile = request.user.userprofile
        if photo :
            if user_profile.profile_photo:
                # Delete the old profile photo
                user_profile.profile_photo.delete()
            user_profile.profile_photo = photo
        user_profile.save()
        # user_profile = UserProfile.objects.get(user=request.user)
        return redirect('profile')
    
    return render(request,"edit_profile.html",data)

def admin_home(request):
    return render(request,"admin_home.html")

def add_station(request):
    if not request.user.is_staff:
        return render(request,'login-register.html')
    valid = False
    if request.method == "POST":
        station_name = request.POST['station_name']
        station_city = request.POST['station_city']
        valid = True
        Station.objects.create(station_name = station_name, station_city = station_city)

    v = {'valid':valid}
    return render(request,'add_station.html',v)

def view_station(request):
    if not request.user.is_authenticated:
        return render(request,"login-register.html")
    data=Station.objects.all()
    d={"data":data}
    return render(request,"view_station.html",d)

def add_train(request):
    if not request.user.is_staff:
        return render(request,'login-register.html')
    valid=False
    data = Station.objects.all()
    if request.method == "POST":
        name = request.POST['trainname']
        train_no= request.POST['train_no']
        from_station = request.POST['from_city']
        to_station= request.POST['to_city']

        departure_time= request.POST['departuretime']
        arival_time = request.POST['arrivaltime']
        travel_time = request.POST['traveltime']
        distance = request.POST['distance']
        fare = request.POST['fare']
        train_image = request.FILES.get('train_photo')
        # i = request.FILES['img']

        source_station = Station.objects.get(station_name = from_station)
        dest_station = Station.objects.get(station_name = to_station)

        
        new_train = Train.objects.create(trainname=name,from_station=source_station,to_station=dest_station,departuretime=departure_time,arrivaltime=arival_time,traveltime=travel_time,distance=distance,fare = fare,train_image=train_image)

        Route.objects.create(train=new_train,station=source_station,fare=0,traveltime=0,distance=0)

        Route.objects.create(train=new_train,station=dest_station,fare=fare,traveltime=travel_time,distance=distance)
        valid=True
    v={"valid":valid,"data":data}
    return render(request,'add_train.html',v,)

def remove_train(request,trainname):
    train = Train.objects.get(trainname = trainname)
    train.delete()
    return redirect("view_train")

def update_train(request,trainname):
    train = Train.objects.get(trainname = trainname)
    stations = Station.objects.all()
    valid=False
    if request.method == "POST":
        #get old source and destination
        old_from_station = train.from_station
        old_to_station = train.to_station
        old_train = train
        name = request.POST['trainname']
        # train_no= request.POST['train_no']
        from_station = request.POST['from_city']
        to_station= request.POST['to_city']

        departure_time= request.POST['departuretime']
        arival_time = request.POST['arrivaltime']
        travel_time = request.POST['traveltime']
        distance = request.POST['distance']
        fare = request.POST['fare']
        train_image = request.FILES.get('train_photo')
        # i = request.FILES['img']
        source_station = Station.objects.get(station_name = from_station)
        dest_station = Station.objects.get(station_name = to_station)
        train.trainname = name
        train.from_station=source_station
        train.to_station=dest_station
        train.arrivaltime=arival_time
        train.departuretime=departure_time
        train.traveltime=travel_time
        train.fare=fare
        if train_image is not None :
            train.train_image = train_image
        train.distance = distance
        train.save()
        #get old source and destination
        # old_source=Station.objects.get(station_name=old_from_station)
        # old_dest=Station.objects.get(station_name=old_to_station)

        route1 = Route.objects.get(train=old_train,station = old_from_station)
        route2=Route.objects.get(train=old_train,station=old_to_station)

        route1.delete()
        route2.delete()
        
        # new_train = Train.objects.create(trainname=name,from_station=source_station,to_station=dest_station,departuretime=departure_time,arrivaltime=arival_time,traveltime=travel_time,distance=distance,fare = fare,train_image=train_image)

        Route.objects.create(train=train,station=source_station,fare=0,traveltime=0,distance=0)

        Route.objects.create(train=train,station=dest_station,fare=fare,traveltime=travel_time,distance=distance)
        valid = True
    data = {"train":train,"stations":stations,"valid":valid}
    return render(request,"update_train.html",data)

def view_train(request):
    if not request.user.is_authenticated:
        return render(request,"login-register.html")
    data=Train.objects.all()
    d={"data":data}
    return render(request,"view_train.html",d)

def add_route(request) : 
    if not request.user.is_staff :
        return render(request,"login-register.html")
    
    stations = Station.objects.all()
    trains = Train.objects.all()
    
    valid = request.GET.get('valid', False)
    if request.method == "POST" :
        station_name = request.POST['station']
        train_name = request.POST['train']
        fare = request.POST['fare']
        traveltime = request.POST['travel_time']
        distance = request.POST['distance']

        station = Station.objects.get(station_name=station_name)
        train = Train.objects.get(trainname=train_name)
        route = Route.objects.create(station = station,train = train,fare = fare,traveltime=traveltime,distance=distance)
        valid=True

        # return redirect('add_route')

    dictionary = {"stations":stations,"trains":trains,"valid":valid}
    return render(request,"add_route.html",dictionary)

def search_train(request):
    stations = Station.objects.all()
    is_searched = False
    trains = []
    date = None
    if request.method == "POST": 
        source = request.POST['source']
        destination = request.POST['destination']
        date = request.POST['date']
        routes = Route.objects.all()
        is_searched = True

        for route1 in routes : 
            for route2 in routes :
                if route1.station.station_name == source and route2.station.station_name == destination and route1.train.trainname == route2.train.trainname :
                    train = Train.objects.get(trainname=route1.train.trainname)
                    train.fare = abs(route1.fare - route2.fare)
                    train.from_station = route1.station
                    train.to_station = route2.station
                    trains.append(train)
    data = {"stations":stations,"is_searched":is_searched,"trains":trains,"date":date}
    return render(request,"search_train.html",data)


def generate_pdf(ticket):
    buffer = BytesIO()

    # Define custom page size
    page_width, page_height = 250, 310
    doc = SimpleDocTemplate(buffer, pagesize=(page_width, page_height))

    # Define data for the ticket
    data = [
        ["Ticket Details:", ""],
        ["Train Name:", ticket.passenger.train.trainname],
        ["Passenger Name:", ticket.passenger.name],
        ["Passenger Age:", str(ticket.passenger.age)],
        ["From:", ticket.from_station],
        ["To:", ticket.to_station],
        ["Date:", str(ticket.passenger.date)],
        ["Fare:", str(ticket.fare)],
    ]

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    # Create table
    table = Table(data)
    table.setStyle(table_style)

    # Build PDF
    elements = []
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer


def book_ticket(request,trainname,fare,source,destination,date): 
    if request.method == "POST" : 
        train = Train.objects.get(trainname = trainname)
        name = request.POST['name']
        age = request.POST['age']
        # train.fare = 
        # train,name,age,date
        fare = Decimal(fare)
        passenger = Passenger.objects.create(train=train, name=name, age=age, date=date)
        passenger.user.add(request.user)
        ticket = Ticket.objects.create(passenger=passenger,from_station=source,to_station=destination,fare=fare)
        # Generate PDF
        pdf_buffer = generate_pdf(ticket)
        
        # Define suggested filename
        filename = f"{ticket.passenger.name}_ticket.pdf"  # You can customize the filename here
        
        # Return PDF content as response with suggested filename
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'
        return response
        
    return render(request,"book_ticket.html")


def booking_history(request) : 
    tickets = Ticket.objects.filter(passenger__user=request.user)
    data = {"tickets" : tickets}
    return render(request,"booking_history.html",data)

def download_ticket(request,id):
    ticket = Ticket.objects.get(pk=id)
    pdf_buffer = generate_pdf(ticket)
        
    # Define suggested filename
    filename = f"{ticket.passenger.name}_ticket.pdf"  # You can customize the filename here
    
    # Return PDF content as response with suggested filename
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'
    return response


def cancel_ticket(request,id):
    ticket = Ticket.objects.get(pk=id)
    ticket.delete()
    return redirect('booking_history')
    
    