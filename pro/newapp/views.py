from django.shortcuts import render,redirect
from newapp.models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import  json

# Create your views here.
def home(request):
    products=Product.objects.filter(Trending=1)
    return render(request,"home.html",{"products":products})

def login_page(request):
    if request.user.is_authenticated:
         return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Login Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name Or Password")
                return redirect("/login")
        return render(request,"login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout (request)
        messages.success(request,"Logout Successfully")
        return redirect("/")
    
def add_to_cart(request):
    if request.headers.get('X-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Add To Card Success'},status=200)
                    else:
                        return JsonResponse({'status':'Product Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Card'},status=200)
    else:
        return JsonResponse({'status':'Invalid'},status=200)

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success !")
            return redirect("login")
    return render(request,"register.html",{"form":form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"collections.html",{"Catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(Category__name=name)
        return render(request,"products/index.html",{"products":products,"Category_name":name})
    else:
        messages.warning(request,"No Such Product Found")
        return redirect("collections")
    
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"products/product_details.html",{"products":products})
        else:
            messages.error(request,"No Product Found")
            return redirect('collections')
    else:
        messages.error(request,"No Catagory Found")
        return redirect('collections')