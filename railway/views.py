from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import *
from django.urls import reverse
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
            user=request.user,
            mobile=mobile_no,
            gender=gender,
            dob =dob
        )
        
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
        # user = authenticate(username=uname,password=password)
        # try :
        #     if user is not None :
        #         if user.is_staff :
        #             login(request,user)
        #             staff = True
        #         elif user :
        #             login(request,user)
        #             passanger = True
        #     else :
        #         invalid_user = True
        # except :
        #     invalid_user = True
        # user = None
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
    return render(request,"user_profile.html")

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
        from_city = request.POST['from_city']
        to_city= request.POST['to_city']
        departure_time= request.POST['departuretime']
        arival_time = request.POST['arrivaltime']
        travel_time = request.POST['traveltime']
        distance = request.POST['distance']
        # i = request.FILES['img']

        Train.objects.create(trainname=name,from_city=from_city,to_city=to_city,departuretime=departure_time,arrivaltime=arival_time,traveltime=travel_time,distance=distance)
        valid=True
    v={"valid":valid,"data":data}
    return render(request,'add_train.html',v,)

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
    stations = Station.objects.all();
    data = {"stations":stations}

    return render(request,"search_train.html",data)