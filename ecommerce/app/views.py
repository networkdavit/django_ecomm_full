from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from . models import Product, Customer, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.
# def any_view(request):
#     user = request.user
#     add=Customer.objects.filter(user=user)
#     cart_items=Cart.objects.filter(user=user)
#     total_item_quantity = Cart.objects.values_list('quantity')
#     item_count = 0
#     print(total_item_quantity, "total_item_quantity")
#     for item in total_item_quantity:
#         for quantity in item:
#             item_count += quantity
#     famount = 0
    
#     print("HERE", cart_items)

#     for p in cart_items:
#         value = p.quantity * p.product.discounted_price
#         famount = famount + value
#     totalamount = famount + 2500
#     print("HERE", item_count)

def cart_item_count(request):
    #get total count of items
    pass

def home(request):
    item_count = 0
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

def about(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

def contact(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))

    return render(request, "app/contact.html", locals())

class CategoryView(View):
    def get(self, request, val):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())

class CategoryTitle(View):
    def get(self, request, val):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html",locals())

class ProductDetail(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registration successull")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/customerregistration.html", locals())

class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile saved successfully")        
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/profile.html", locals())

def address(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", locals())

class UpdateAddress(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))

        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add) 
        return render(request, "app/updateAddress.html", locals())
    def post(self, request, pk):
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
            messages.success(request, "Congratulations! Profile updated successfully")        
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def add_to_cart(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0 
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 2500

    return render(request, "app/addtocart.html", locals())

def plus_cart(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        print("?Asdfsadf")
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))        
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 2500
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        print("?Asdfsadf")
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))        
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 2500
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.user.is_authenticated:
        item_count = len(Cart.objects.filter(user=request.user))
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))        
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 2500
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def payment_complete(request):
    user = request.user
    return render(request, "app/payment_complete.html", locals())

class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            item_count = len(Cart.objects.filter(user=request.user))
        user = request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        total_item_quantity = Cart.objects.values_list('quantity')
        item_count = 0
        print(total_item_quantity, "total_item_quantity")
        for item in total_item_quantity:
            for quantity in item:
                item_count += quantity
        famount = 0
        
        print("HERE", cart_items)

        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 2500
        print("HERE", item_count)
        return render(request, "app/checkout.html", locals())