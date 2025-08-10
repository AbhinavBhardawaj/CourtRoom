from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib import messages
from users.forms import CustomSignupForm
# Create your views here.

User = get_user_model()
def login_view(request):
    # if request.method == "POST":
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     try:
    #         user = .objects.get(email=email)
    #         user = authenticate(request, username=user.username, password=password)
            
    #         if user is not None:
    #             login(request,user)
    #             messages.success(request, "Login successful!")
    #             return redirect('home')
            
    #         else:
    #             messages.error(request,'Invalid email or password.')

    #     except User.DoesNotExist:
    #         messages.error(request,'User with this email does not exist.')
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
            user = authenticate(request,username = user.username,password = password)

            if user is not None:
                login(request,user)
                messages.success(request,'Login Successful!')
                return redirect('home')

            else:
                messages.error(request,'Invalid email or password!')
        except User.DoesNotExist:
            messages.error(request,'User with this email does not exist.')
    
    return render(request,'users/login.html')

def signup(request):
    if request.method == "POST":
        print("Form is being submitted") 
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request,'Account created successfully!')
            return redirect('login')

        else:
            print(form.errors)
            messages.error(request,'Please correct the below.')
    
    else:
        form = CustomSignupForm()

    return render(request,'users/signup.html',{'form':form})

def forgotpswd(request):
    return render(request,'Users/forgotpswd.html')

def newpswd(request):
    return render(request,'Users/newpasswd.html')

def pswd_reset_done(request):
    return render(request,'Users/pswd_reset_done.html')