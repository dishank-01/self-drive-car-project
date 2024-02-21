from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from selfdriveapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import  messages

# Create your views here.
def register(request):
    const={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            const['errormsg']="field cannot be empty"
            return render(request,"register.html",const)
        elif upass!=ucpass:
            const['errormsg']="password not matching"   #to make password validation it will not let you enter different values
            return render(request,'register.html',const)
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass) #to make password protected and encrypted in database
                u.save()
                const['success']="user added succssfully"
                return render(request,'register.html',const)
            except Exception:
                const['errormsg']="username already exist"
                return render(request,'register.html',const)
    else:
        return render(request,'register.html')


def user_login(request):
     context={}
     if request.method=='POST':
        
          Uname=request.POST['uname']
          Upass=request.POST['upass']
          if Uname=="" or Upass=="":
               context['errormsg']="Feild cant be empty"
               return render(request,'login.html',context)
          else:
               u=authenticate(username=Uname,password=Upass)#authenticate is inbuild function
               # print(u)
               if u is not None:# means uname and pwd are correct
                    login(request,u)
                    return redirect('/home')#here we need to give url not a function
               else: #if user is not authenticatet then gives error msg
                    context['errormsg']="Invalid username and password"
                    return render(request,'login.html',context)
     else:
          return render(request,'login.html') 
            
    
def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    #userid=request.user.id
    #print("id of login user",userid)
  #  print("result",request.user.is_authenticated)   #to show in terminal whether  the user is logged or not and result in true or none
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(category=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)    
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("order id is:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    for x in orders:
        s=s+x.pid.price * x.qty
        context={}
        context['n']=np
        context['products']=orders
        context['total']=s
    return render(request,"placeorder.html",context)
    
def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def cart(request):
    return render(request,'cart.html')
    
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)#user->name of module
        print(u[0])
        p=Product.objects.filter(id=pid)
        print(p[0])
        c=Cart.objects.create(uid=u[0],pid=p[0])#to add pid and uid to cart table,we want 1st inex i.e. id from both table 
          #id lies on index 0
        c.save()
        return HttpResponse("product added to cart")
    else:
        return redirect('/login')
    
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("order id is:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    for x in orders:
        s=s+x.pid.price * x.qty
        context={}
        context['n']=np
        context['products']=orders
        context['total']=s
    return render(request,"placeorder.html",context)

def viewcart(request):
    userid=request.user.id #to fetch id
    c=Cart.objects.filter(uid=userid) #filter then objects available for particular user will show in viewcart
    s=0
    np=len(c) #all product avalable in c ==>> to check how much product in cart
    for x in c:
          # print(x)
          # print(x.pid.price)
          s=s+x.pid.price*x.qty #0+3000 formula should be under for loop
    context={}
    context['products']=c
    context['n']=np
    context['total']=s
    return  render(request,'cart.html',context)

def makepayment(request):  
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_fAyquKMApagg9t", "bAmBIz9EhbsTk3zwJjjMusny"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def user_logout(request):
    logout(request)
    return redirect("/homepage")

def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        new_password = request.POST.get('upass')
        confirm_password = request.POST.get('cupass')

        user = User.objects.filter(username=username).first()

        if user:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                # Update the session to avoid automatic logout
                update_session_auth_hash(request, user)

                messages.success(request, 'Password reset successfully!')
                return redirect('/login')  # Redirect to login page after successful password reset
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'User not found.')
    return render(request,'forget.html')
                          