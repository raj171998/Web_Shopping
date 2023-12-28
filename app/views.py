from django.shortcuts import render, redirect
from django.views import View 
from app.models import Product, Customer, Cart, OrderPlaced
from app.forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings 

# Create your views here.


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles': mobiles,'totalitem':totalitem})

# def product_details(request):
#     return render(request, 'app/productdetails.html')

@method_decorator(login_required, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        product_already_in_cart = False
        product_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return  render(request, 'app/productdetails.html', {'product':product,'product_already_in_cart':product_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):

    user = request.user
    product_id = request.GET.get('prod_id')
    product  = Product.objects.get(id=product_id)
    reg = Cart(user=user, product=product)
    reg.save()

    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        totalitem = len(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [ p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
            total_amount = amount + shipping_amount
            print(total_amount)
            return render(request, 'app/show_cart.html',{'carts':cart,'amount':amount,'total_amount':total_amount,'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }

        return JsonResponse(data)

def minus_cart(request):
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id)& Q( user = request.user))
        c.quantity-=1
        c.save()
        amount = 0.0 
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
        data = {
            'quantity':c.quantity,
            'amount' : amount,
            'total_amount':total_amount
        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method=="GET":
        totalitem = 0
        prod_id = request.GET['prod_id']
        c =  Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount +=tempamount
        total_amount = amount + shipping_amount


        data={
            'amount':amount,
            'total_amount':total_amount,
            'totalitem': totalitem
            }
        return JsonResponse(data)



def buy_now(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product  = Product.objects.get(id=product_id)
    reg = Cart(user=user, product=product)
    reg.save()
    return redirect('/checkout')


# def profile(request):
#     return render(request, 'app/profile.html')

@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
    def get(self,request):
        totalitem=0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, state=state, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations !!! Profile Updated Successfully...")
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

@login_required
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'address':address,'active':'btn-primary'})

@login_required
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

# def change_password(request):
#     return render(request, 'app/changepassword.html')

@login_required
def mobile(request, data=None):
    totalitem = 0
    if data == None:
        mobiles = Product.objects.filter(category="M") 
    elif data == "Realme" or data == "Redmi" or data=="Samsung" or data=="i-Phone" or data == "OnePlus" or data=="Moto" or data=="Oppo":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=17000)
    elif data == 'greater':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=17000)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def login(request):
    return render(request, 'app/login.html')

def registration(request):
    if request.method=="POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request," Congratulation !!! Registered Seccessfully...")
            form.save()
        return render(request, 'app/customer_registration.html',{'form':form}) 
    form = CustomerRegistrationForm()
    return render(request, 'app/customer_registration.html',{"form":form})

# class CustomerRegistrationView(View):
#     def get(self, request):
#         form = CustomerRegistrationForm()
#         return render(request, 'app/customer_registration.html', {'form' : form})
    
#     def post(self, request):
#         form = CustomerRegistrationView(request.POST)
#         if form.is_valid():
#             form.save()
#         return render(request, 'app/customer_registration.html',{'form':form})
        


class Checkout(View):
    def get(self, request):

        totalitem = 0
        user = request.user
        address = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        for cart in cart_items:
            tempamount = (cart.quantity * cart.product.discounted_price)
            amount +=tempamount
        total_amount = amount + shipping_amount 
        totalamount = total_amount *100      
        return render(request, 'app/checkout.html',locals()) 


@login_required
def payment_done(request):
    if request.method == 'GET':
        cust_id = request.GET.get('custid')
        user = request.user
        customer = Customer.objects.get(id=cust_id)
        carts = Cart.objects.filter(user=user)
        for cart in carts:
            OrderPlaced(user=user, customer=customer, product=cart.product, quantity=cart.quantity).save()
            cart.delete()
        return redirect('orders')