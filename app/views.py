from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.views import View
from . models import Product, Customer, Cart, Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm, PaymentInitForm
from django.contrib import messages
from django.db.models import Q
# from django.urls import reverse
from django.conf import settings
import json
import requests


api_key = settings.PAYSTACK_TEST_SECRET_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

def contact(request):
     totalitem = 0
     wishitem = 0
     if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
     return render(request, "app/contact.html", locals())

class CategoryView(View):
    def get(self,request,val):
         totalitem = 0
         wishitem = 0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
         product = Product.objects.filter(category=val)
         title = Product.objects.filter(category=val).values('title')
         return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self,request,val):
         totalitem = 0
         wishitem = 0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
         product = Product.objects.filter(title=val)
         title = Product.objects.filter(category=product[0].category).values('title')
         return render(request, "app/category.html", locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
        return render(request, 'app/productdetail.html',locals())
    
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
            
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
            
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations! Profile Save Successfully')
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html', locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
            
        return render(request, 'app/updateAddress.html', locals())
        
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount= 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        tax = 250
        amount = amount + value
    totalamount = amount + 2000 + tax
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user)) 
        
    return render(request, 'app/addtocart.html', locals())

# def show_wishlist(request):
#     user = request.user
#     wishlist = Wishlist.objects.filter(user=user)
#     amount = 0
#     for p in wishlist:
#         # value = p.quantity*p.product.discounted_price
#         # amount = amount + value
        
#         totalitem = 0
#         wishitem = 0
    
      
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem = len(Wishlist.objects.filter(user=request.user)) 
        
    
#     return render(request, 'app/wishlist.html', locals())

class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
            
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
            tax = 250
        totalamount = famount + 2000 + tax
        return render(request, 'app/checkout.html', locals())
    
# def orders(request):
#     order_placed=OrderPlaced.objects.filter(user=request.user)
#     return render(request, 'app/orders.html', locals())
    

def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            tax = 250
            amount = amount + value 
        totalamount = amount + 2000  + tax
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':totalamount            
        }
        return JsonResponse(data)
    
        
def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            tax = 250
            amount = amount + value 
        totalamount = amount + 2000 + tax
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':totalamount            
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) &  Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            tax = 250
            amount = amount + value 
        totalamount = amount + 2000  + tax
        data ={
            'amount': amount,
            'totalamount':totalamount            
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user)) 
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())
            
    
    
    
# def payment_init(request):
#     if request.method == 'POST':
#         # get form data if POST request
#         form = PaymentInitForm(request.POST)

#         # validate form before saving
#         if form.is_valid():
#             payment = form.save(commit=False)
#             payment.save()
#             # set the payment in the current session
#             request.session['payment_id'] = payment.id
#             # message alert to confirm payment intializaton
#             messages.success(request, "Payment Initialized Successfully." )
#             # redirect user for payment completion
#             return redirect(reverse('payment:process'))
    # else:
    # # render form if GET request
    #     form = PaymentInitForm()
    # return render(request, 'payment/create.html', {'form': form})
def payment_process(request):
    # retrive the payment_id we'd set in the djago session ealier
    payment_id = request.session.get('payment_id', None)
    # using the payment_id, get the database object
    payment = get_object_or_404(payment, id=payment_id)
    # retrive payment amount 
    amount = payment.get_amount()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:success'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))

        # metadata to pass additional data that 
        # the endpoint doesn't accept naturally.
        metadata= json.dumps({"payment_id":payment_id,  
                              "cancel_action":cancel_url,   
                            })

        # Paystack checkout session data
        session_data = {
            'email': payment.email,
            'amount': int(amount),
            'callback_url': success_url,
            'metadata': metadata
            }

        headers = {"authorization": f"Bearer {api_key}"}
        # API request to paystack server
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()
        if response["status"] == True :
            # redirect to Paystack payment form
            try:
                redirect_url = response["data"]["authorization_url"]
                return redirect(redirect_url, code=303)
            except:
                pass
        else:
            return render(request, 'payment/process.html', locals())
    else:
        return render(request, 'payment/process.html', locals())
    
def payment_success(request):
    return render(request, 'payment/success.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
