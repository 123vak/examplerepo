from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.db import connection
from django.contrib.auth import logout



def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'loginid' not in request.session:
            return redirect('login')  
        return view_func(request, *args, **kwargs)  
    return _wrapped_view

@login_required
def mainpage(request):
    if request.session['loginid']:
        return render(request, 'LoginLogout/mainpage.html',{'logintype': request.session['loginid']})  
    else:
        return render(request, 'LoginLogout/login.html', {'captcha_key': captcha_key})

@login_required
def dashboard_view(request):
    print(request.session['loginid'])
    if request.session['loginid']:
        return render(request, 'LoginLogout/dashboard.html',{'logintype': request.session['loginid']})  
    else:
            return render(request, 'LoginLogout/login.html', {'captcha_key': captcha_key})

def user_Logout(request):
    print(request.session)
    request.session.flush()
    logout(request)
    print(request.session)
    return redirect('login')  


def captcha_refresh(request):
    print('storedkye: ',request.session['captcha_key'])
    captcha_key = CaptchaStore.generate_key()
    request.session['captcha_key'] = captcha_key
    captcha_image_url = captcha_image_url(captcha_key)
    return JsonResponse({'captcha_key': captcha_key, 'captcha_image_url': captcha_image_url})


def generate_captcha(request):
    # if 'captcha_key' not in request.session:
    captcha_key = CaptchaStore.generate_key() 
    request.session['captcha_key'] = captcha_key
    # else:
    #     captcha_key = request.session['captcha_key']  
    return captcha_key


def handle_form_submission(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    captcha_response = request.POST.get('captcha')  

    stored_captcha_key = request.session.get('captcha_key')

    if not verify_captcha(captcha_response, stored_captcha_key):
        captcha_key = generate_captcha(request) 
        return render(request, 'LoginLogout/login.html', {'error': "Invalid Captcha", 'captcha_key': captcha_key})
    
    user_info = authenticate_user(username, password)

    if user_info:
        request.session['loginid'] = user_info['loginid']
        request.session['logintype'] = user_info['logintype']
        return redirect('dashboard')
    else:
        captcha_key = generate_captcha(request)  
        return render(request, 'LoginLogout/login.html', {'error': "Invalid Username or Password", 'captcha_key': captcha_key})

def User_Login(request):
    if request.method == 'POST':
        return handle_form_submission(request)  

    else:
        captcha_key = generate_captcha(request)
        return render(request, 'LoginLogout/login.html', {'captcha_key': captcha_key})

def verify_captcha(captcha_response, stored_captcha_key):
    try:
        captcha = CaptchaStore.objects.get(hashkey=stored_captcha_key)
        print("user: ",captcha_response)
        print("System: ",captcha.response)
        if captcha_response.lower() == captcha.response.lower():
            return True
    except CaptchaStore.DoesNotExist:
        return False
    return False


def authenticate_user(username, password):
    try:
        with connection.cursor() as cursor1:
            cursor1.callproc('Login_Chk',[username, password])
            row = cursor1.fetchone()
            print("row:", row)
            if row:
                return{
                    'loginid':row[0],
                    'logintype':row[1],
                }
    except Exception as e:
        print(e)
        
    # return None
    # try:
    #     # import requests

    #     # Define the URL of the API
    #     url = "http://localhost:5000/api/user"  

    #     # Define the data to send as a JSON body
    #     data = {
    #         "Username": username,
    #         "Password": password
    #     }

    #     # Send a POST request
    #     response = requests.post(url, json=data)

    #     # Print the response
    #     if response.status_code == 200:
    #         print("Response:", response.json()) 
    # except Exception as e:
    #     print(e)
       