from datetime import datetime
from pyclbr import Class

from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from app.forms import newUserForm
from app.models import Product, Promotion, Comments

currentCart = []


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


def productsManagement(request):
    products = Product.objects.all()

    form = {'products': products}

    return render(request, 'productsManagement.html', form)


def createProduct(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST' and 'img01' in request.FILES:
        name = request.POST['name']
        price = request.POST['price']
        description_ = request.POST['description']
        imagem = request.FILES['img01']
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


def promotionsManagement(request):
    promotions = Promotion.objects.all()

    form = {'promotions': promotions}

    return render(request, 'promotionsManagement.html', form)


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
            return render(request, 'promotionsManagement.html')
        else:
            return render(request, 'createPromotion.html', {'error': True})
    else:
        return render(request, 'createPromotion.html', {'error': False})


def updatePromotion(request, pk):
    promotion = Promotion.objects.get(id=pk)
    if request.method == 'POST':
        promotion.name = request.POST['name']
        promotion.discount = request.POST['discount']
        promotion.description = request.POST['description']
        promotion.deadline = request.POST['deadline']
        promotion.save()
        return render(request, 'promotionsManagement.html')
    return render(request, 'updatePromotion.html', {'promotion': promotion})


def deletePromotion(request, id):
    promotion = Promotion.objects.get(id=id)
    promotion.delete()
    return redirect('promotionsManagement')


def searchProducts(request):
    productsBrands = Product.objects.order_by('brand').values_list('brand', flat=True).distinct()
    brands = {}
    for pB in productsBrands:
        brands[pB] = Product.objects.filter(brand=pB).count()

    # categorias e brands [(, )..]
    listCategoriesAndBrands = Product.objects.order_by('category').values_list('category', 'brand').distinct()

    productsFilter = {}
    for c in listCategoriesAndBrands:
        if c[0] not in productsFilter.keys():
            productsFilter[c[0]] = [c[1]]
        else:
            productsFilter[c[0]].append(c[1])

    # productFilter={}
    # for c in productsCategories:
    #    print(Product.objects.all().filter(category=c).values('brand', 'pk').distinct())
    #    productFilter[c] = Product.objects.all().filter(category=c).values('brand').distinct()

    # print(type(productCategories))

    # obter categorias e brands

    query = ''
    productsList = []
    result = Product.objects.all()
    if request.method == 'POST':
        # home search images click
        if 'Smartphones' in request.POST:
            result = Product.objects.filter(category="Smartphones")
        if 'Televisions' in request.POST:
            result = Product.objects.filter(category="Televisions")
        if 'Drones' in request.POST:
            result = Product.objects.filter(category="Drones")
        if 'Computers' in request.POST:
            result = Product.objects.filter(category="Computers")

        if 'searchBar' in request.POST:
            query = request.POST['searchBar']
            result = Product.objects.filter(name__icontains=query)

        if 'brandsCategories' in request.POST and len(request.POST.getlist('brandsCategories', [])) > 1:
            brandsLstCat = request.POST.getlist('brandsCategories', [])
            for brandCat in brandsLstCat:
                if brandCat != '':
                    productS = Product.objects.filter(
                        brand=brandCat)  # TODO apenas está a ver por BRAND e n por CATEGOYR (no shop.html só envio brand)
                    if len(productS) > 1:
                        for p in productS:
                            productsList.append(p)
                    else:
                        productsList.append(productS)
            result = productsList

        if 'brandsProducts' in request.POST:
            brandsLst = request.POST.getlist('brandsProducts', [])
            for brand in brandsLst:
                if brand != '':
                    products = Product.objects.filter(
                        brand=brand)
                    if len(products) > 1:
                        for p in products:
                            productsList.append(p)
                    else:
                        productsList.append(products)
            result = productsList

        if 'priceRange' in request.POST:
            minPrice = request.POST['minPrice']
            maxPrice = request.POST['maxPrice']
            result = Product.objects.filter(price__range=[minPrice, maxPrice])

    tparams = {'productsFilter': productsFilter,
               'totalBrands': Product.objects.values('brand').distinct().count(),
               'totalCategories': Product.objects.values('category').distinct().count(),
               'brands': brands,
               'productsList': result
               }

    return render(request, 'shop.html', tparams)


def home(request):
    assert isinstance(request, HttpRequest)
    result = Product.objects.all()[0:3]
    tparams = {'productsList': result}

    if request.method == 'POST' and request.user.is_authenticated:
        userName = request.POST['username']
        userEmail = request.POST['userEmail']
        description = request.POST['description']
        rating = request.POST['rating']
        if userName and userEmail and description:

            comment = Comments(userName=userName, userEmail=userEmail, description=description, rating=rating)
            comment.save()
            tparams = {'productsList': result,
                       'commentSuccess': True}
            return render(request, 'index.html', tparams)
        else:
            return render(request, 'index.html', {'productsList': result, 'error': True})
    else:
        tparams = {'productsList': result,
                   'userNotLogged': True}
        return render(request, 'index.html', tparams)


# TODO

def checkout(request):
    assert isinstance(request, HttpRequest)
    iphoneX = Product.objects.get(name="iPhone X")
    currentCart = iphoneX
    tparams = {
        'cart': currentCart
    }

    return render(request, 'checkout.html', tparams)


def cart(request):
    assert isinstance(request, HttpRequest)
    iphoneX = Product.objects.get(name="iPhone X")
    currentCart = [iphoneX]
    tparams = {
        'cart': currentCart
    }

    return render(request, 'cart.html', tparams)
