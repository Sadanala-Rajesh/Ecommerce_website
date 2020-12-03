from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib import sessions
from Ecommers_app.models import Products,User_Cart
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail 



def Home_page(request):
	return render(request,'home.html')

def login_page(request):
	if request.method == "POST":
		
		user_name = request.POST['user_name']
		request.session['username'] = user_name
		password = request.POST['password1']

		user = auth.authenticate(username=user_name,password=password)
		if user is not  None:
			auth.login(request,user)
			print('loginpage')
			return redirect("/accounts/display_products/")
		else:
			messages.info(request,"Enter valid details")
			return redirect("/accounts/login/")
	else:
		return render(request,"login.html")

def logout_page(request):
	auth.logout(request)
	return redirect('/')


def register(request):
	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		user_name = request.POST['user_name']
		email = request.POST['email']
		password = request.POST['password1']
		password1 = request.POST['password2']
		if password == password1:
			if User.objects.filter(username=user_name).exists():
				messages.info(request,"user_name already exist use another")
				return redirect('/accounts/register/')
			elif User.objects.filter(email=email).exists():
				messages.info(request,"email already exist use another")
				return redirect('/accounts/register/')
			else:
				user=User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email,password=password)
				user.save()
				messages.info(request,"New account created")
				return redirect('/accounts/register/')
		else:
			print('passwords are not same')
			messages.info(request," password and confirm_password are must be same")
		return redirect('/accounts/register/')
	else:
		return render(request,'registration.html')


@login_required(login_url='/accounts/login/')
def display_Products(request):
	P_data = Products.objects.all()
	return render(request, 'd_products.html',{'images' : P_data})

@login_required(login_url='/accounts/login/')
def Products_add_to_cart(request,name):
	lst=[]
	data= Products.objects.filter(P_name=name)
	for i in data:
		lst.append(i.P_name)
		lst.append(i.P_image)
		lst.append(i.P_price)

	username1 = request.session['username']
	data2=User.objects.get(username=username1)
	User_Cart.objects.create( user=data2,P_name=lst[0],P_image=lst[1],P_price=lst[2])
	messages.info(request,"Product add to cart")
	return redirect('/accounts/display_products/')
@login_required(login_url='/accounts/login/')
def display_user_cart_details(request):
	if request.session.has_key('username'):
		username1 = request.session['username']
		P_data = User_Cart.objects.filter(user__username=username1)
		return render(request, 'user_cart_details.html',{'images' : P_data})
	else:
		return redirect('/accounts/login')


@login_required(login_url='/accounts/login')
def Send_mail_to_Buyer(request,name):

	if request.method == 'POST':
		first_name = request.POST['Phone_Number']
		gmail= request.POST['Mail_id']
		user_name = request.POST['Address']
		lst=[]
		data= Products.objects.filter(P_name=name)

		for i in data:
			lst.append(i.P_name)
			lst.append(i.P_image)
			lst.append(i.P_price)
		username1 = request.session['username']
		subject = 'Ecommers Website'
		message = f'Hi {username1},your product:{lst[0]},Product price:{lst[2]},thank you for Order product.'
		email_from = settings.EMAIL_HOST_USER 
		recipient_list = [gmail,]
		send_mail( subject, message, email_from, recipient_list )
		messages.info(request,"Product delivered soon")
		User_Cart.objects.filter(P_name=name).delete()
		return redirect('/accounts/display_products/')
	data= Products.objects.filter(P_name=name)


	return render(request,'send_mail.html',{'images':data})


	
	