from datetime import datetime
from pyclbr import Class

from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from app.forms import newUserForm
from app.models import Product, Promotion


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('user')
            password = request.POST.get('pass')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                loginUser(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered')
        return redirect('home')
    else:
        form = newUserForm()
        if request.method == 'POST':
            form = newUserForm(request.POST)
            if form.is_valid():
                form.save()
                # clean field
                user = form.cleaned_data.get('username')
                # messages (dict)
                messages.success(request, 'Account was created for ' + user)

                return redirect('home')

        return render(request, 'signup.html', {'form': form})


def logout(request):
    logoutUser(request)
    return redirect('home')


def createProduct(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description_ = request.POST['description']
        imagem = request.FILES.get('imagem')
        quantity = request.POST['quantity']
        stock = request.POST['stock']
        brand = request.POST['brand']
        category = request.POST['category']

        # PROMOTION (obj) AND IMAGE ARE NOT WORKING!!!
        promotion_ = request.POST.get('promo')
        print(type(promotion_))
        try:
            obj = Promotion.objects.get(name=promotion_)
        except Promotion.DoesNotExist:
            obj = None

        if stock == 'on':
            stock = True
        else:
            stock = False

        if 'name' and 'price':
            product = Product(name=name, price=price, description=description_, image=imagem, quantity=quantity,
                              stock=stock, brand=brand, category=category, promotion=obj)
            product.save()
            return render(request, 'shop.html')
        else:
            return render(request, 'createProduct.html', {'error': True})

    promotion = Promotion.objects.all()
    return render(request, 'createProduct.html', {'promotion': promotion})


def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description_ = request.POST['description']
        product.imagem = request.FILES.get('imagem')
        product.quantity = request.POST['quantity']
        product.stock = request.POST['stock']
        product.brand = request.POST['brand']
        product.category = request.POST['category']

        promotion_ = request.POST.get('promo')
        print(type(promotion_))
        try:
            obj = Promotion.objects.get(name=promotion_)
        except Promotion.DoesNotExist:
            obj = None

        if product.stock == 'on':
            product.stock = True
        else:
            product.stock = False

        product.save()
        return render(request, 'shop.html')
    return render(request, 'updateProduct.html', {'product': product})


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('productsManagement')









def createPromotion(request):
    assert isinstance(request, HttpRequest)

    if 'name' in request.POST and 'discount' in request.POST:
        name_ = request.POST['name']
        discount_ = request.POST['discount']
        description_ = request.POST['description']
        deadline_ = request.POST['date']
        if name_ and discount_:

            promotion = Promotion(name=name_, discount=discount_, description=description_, deadline=deadline_)
            promotion.save()
            return render(request, 'createProduct.html')
        else:
            return render(request, 'createPromotion.html', {'error': True})
    else:
        return render(request, 'createPromotion.html', {'error': False})


def productsManagement(request):
    products = Product.objects.all()

    form = {'products': products}

    return render(request, 'productsManagement.html', form)


def home(request):
    assert isinstance(request, HttpRequest)
    tparams = {}
    return render(request, 'index.html', tparams)

    return render(request, 'signup.html', tparams)


def shop(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'shop.html', tparams)


def productDetails(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'product-details.html', tparams)


def checkout(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'checkout.html', tparams)


def cart(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'cart.html', tparams)
