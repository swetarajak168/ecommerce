from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

#def home(request):
 #return render(request, 'app/home.html')
class ProductView(View):
   def get(self, request):
    Laptop = Product.objects.filter(category='L')
    Mobile = Product.objects.filter(category='M')
    Earphone = Product.objects.filter(category='E')
    Speaker = Product.objects.filter(category='S')
    return render (request,'app/home.html',
    {'Laptop':Laptop, 'Mobile':Mobile,'Earphone':Earphone,
    'Speaker':Speaker} )
#def product_detail(request):
 #return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
     product= Product.objects.get(pk=pk)
     return render(request,'app/productdetail.html',{'product':product} )
def add_to_cart(request):
 user =request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id = product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart' )

def show_cart(request):
   if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user  ]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
            totalamount = amount+ shipping_amount
        return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount, 'amount':amount})
    else:
       return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
            
        data ={
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount+ shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
 
              
        data ={
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount+ shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product= prod_id) & Q(user = request.user))
        
        c.delete()
        amount = 0.0
        shipping_amount = 100.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
        
              
        data ={
                
                'amount':amount,
                'totalamount': amount+ shipping_amount
            }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
  add = Customer.objects.filter(user = request.user)
  return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
        
        return render(request, 'app/mobile.html', {'mobiles': mobiles})



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',
        {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',
        {'form':form})

def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user) 
  cart_items =  Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount = 100.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount 
    totalamount= amount +shipping_amount

  return render(request,'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

def payment_done(request):
    user = request.user 

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form': form, 'active':'btn-primary'})
        

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Customer(user= usr, name=name, locality= locality,city= city, state= state)
            reg.save()
            messages.success(request,'profile updated successfully')
        return render(request,'app/profile.html',{'form': form, 'active':'btn-primary'})


