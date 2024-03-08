from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def home(request) : 
    return render(request,'index.html')

def login(request) : 
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

        try:
            user = authenticate(username=uname,password=password)
            if user is None : 
                invalid_user = True
        except:
            # print("inside the except")
            invalid_user = True
        try:
            if user.is_staff:
                login(request)
                staff = True
            elif user:
                login(request)
                passanger=True
        except Exception as e:
            # Log the exception for debugging
            print(f"An exception occurred during authentication: {e}")
            invalid_user=True
    data = {'passanger':passanger,'staff':staff,'invalid_user':invalid_user,'flag':False}

    return render(request,'login-register.html',data)

def user_home(request) :
    return render(request,'user_home.html')




