from datetime import datetime
from pyclbr import Class

from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from app.forms import newUserForm, paymentForm
# Create your views here.
from app.forms import newUserForm, paymentForm, updateUserForm, createProductForm
from app.models import Product, Promotion, Comment, PaymentMethod, Payment, ShoppingCart, ShoppingCartItem
from django.contrib.auth.models import User
from app.forms import *

from app.forms import CommentForm, ProductForm, PromotionForm

carts = {}


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
                messages.success(request, 'Welcome!!! ')

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
                user = form.cleaned_data.get('username')
                # messages (dict)
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        return render(request, 'signup.html', {'form': form})


def logout(request):
    logoutUser(request)
    return redirect('home')


def usersManagement(request):
    users = User.objects.values()
    return render(request, 'usersManagement.html', {'users': users})


def deleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def updateUser(request):
    tparams = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = updateUserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['username']
                email = data['email']
                curPass = data['currentPassword']
                newPass = data['newPassword']
                newRepeatedPass = data['repeatNewPassword']
                firstName = data['first_name']
                lastName = data['last_name']

                if newPass != newRepeatedPass:
                    form = updateUserForm()
                    tparams['form'] = form
                    tparams['error'] = "Inserted Passwords Are Not The Same"
                    return render(request, 'updateUser.html', tparams)
                if request.user.check_password(curPass):

                    user = request.user
                    user.username = username
                    user.first_name = firstName
                    user.last_name = lastName
                    user.email = email
                    user.set_password(raw_password=newPass)
                    user.save()
                else:
                    form = updateUserForm()
                    tparams['form'] = form
                    tparams['error'] = "Incorrect Password"
                    return render(request, 'updateUser.html', tparams)
                return redirect('login')
        else:
            form = updateUserForm()
        tparams['form'] = form

        return render(request, 'updateUser.html', tparams)
    return redirect('login')


def productInfo(request, id):
    canRev = False
    product = Product.objects.get(id=id)
    comments = Comment.objects.filter(product=product)
    commentsRating = [c.rating for c in comments]
    avg = 0
    tparams = {}

    if commentsRating != []:
        avg = sum(commentsRating) / len(commentsRating)
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['userName']
                email = data['userEmail']
                descr = data['description']
                rating = data['rating']

                com = Comment(userName=username, userEmail=email, description=descr, rating=rating)
                com.product = product
                com.save()

        else:
            form = CommentForm()
        tparams = {}
        shoppingCarts = ShoppingCart.objects.filter(user_id=request.user.id)
        bought = []
        if shoppingCarts:
            for scs in shoppingCarts:
                scis = ShoppingCartItem.objects.filter(cart_id=scs.id)
                bought += [s.product for s in scis]

        if product in bought:
            canRev = True

    tparams['product'] = product
    tparams['comments'] = comments
    tparams['avg'] = round(avg, 1)
    tparams['comNo'] = len(comments)
    tparams['canReview'] = canRev
    tparams['form'] = form
    return render(request, 'productInfo.html', tparams)


def productsManagement(request):
    products = Product.objects.all()

    form = {'products': products}

    return render(request, 'productsManagement.html', form)


def shop(request):
    return render(request, 'shop.html')


def createProduct(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = createProductForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                name = data['name']
                price = data['price']
                description = data['description']
                image = request.FILES['image']
                quantity = data['quantity']
                stock = data['stock']
                brand = data['brand']
                category = data['category']
                promotion = data['promotion']
                pr = Product()
                pr.name = name
                pr.price = price
                pr.description = description
                pr.image = request.FILES["image"]
                pr.quantity = quantity
                pr.stock = stock
                pr.brand = brand
                pr.category = category
                pr.promotion = promotion
                pr.save()
                return redirect('productsManagement')
            else:
                print(form.errors)
        else:
            form = createProductForm()

        return render(request, 'createProduct.html', {'form': createProductForm})
    else:
        redirect('login')

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product.objects.get(id=pk)
            product.name = form.cleaned_data["name"]
            product.price = form.cleaned_data["price"]
            product.description = form.cleaned_data["description"]
            product.image = request.FILES["imageProduct"]
            product.quantity = form.cleaned_data["quantity"]
            product.stock = form.cleaned_data["stock"]
            product.brand = form.cleaned_data["brand"]
            product.category = form.cleaned_data["category"]
            product.promotion = Promotion.objects.get(id=form.cleaned_data["promotion"])


def updateProduct(request, pk):
    pr = Product.objects.get(id=pk)
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = createProductForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                name = data['name']
                price = data['price']
                description = data['description']
                quantity = data['quantity']
                stock = data['stock']
                brand = data['brand']
                category = data['category']
                promotion = data['promotion']
                pr.name = name
                pr.price = price
                pr.description = description
                pr.image = request.FILES["image"]
                pr.quantity = quantity
                pr.stock = stock
                pr.brand = brand
                pr.category = category
                pr.promotion = promotion
                pr.save()
                return redirect('productsManagement')
        else:
            form = createProductForm(initial={
                'name': pr.name,
                'price': pr.price,
                'description': pr.description,
                'image': pr.image,
                'quantity': pr.quantity,
                'stock': pr.stock,
                'brand': pr.brand,
                'category': pr.category,
                'promotion': pr.promotion,
            })
        return render(request, 'updateProduct.html', {'form': form})
    return redirect('login')


def deleteComment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('commentsManagement')


def commentsManagement(request):
    comments = Comment.objects.all()
    form = {'comments': comments}
    return render(request, 'commentsManagement.html', form)


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
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect("login")

    if request.method == "POST":
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = Promotion(name=form.cleaned_data["name"],
                                  discount=form.cleaned_data["discount"],
                                  description=form.cleaned_data["description"],
                                  deadline=form.cleaned_data["deadline"],
                                  )
            promotion.save()
            return redirect("promotionsManagement")
    else:
        form = PromotionForm()
    return render(request, 'createPromotion.html', {"form": form})


def updatePromotion(request, promotion_id):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = Promotion.objects.get(id=promotion_id)
            promotion.name = form.cleaned_data["name"]
            promotion.discount = form.cleaned_data["discount"]
            promotion.description = form.cleaned_data["description"]
            promotion.deadline = form.cleaned_data["deadline"]
            promotion.save()
            return redirect("promotionsManagement")
    else:
        promotion = Promotion.objects.get(id=promotion_id)
        form = PromotionForm(initial={"name": promotion.name,
                                      "discount": promotion.discount,
                                      "description": promotion.description,
                                      "deadline": promotion.deadline,
                                      })
    return render(request, "updatePromotion.html", {"form": form})


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

    #####################
    # list_Products = []
    # for c in listCategoriesAndBrands:
    #    list_Products.append(Product.objects.filter(category=c[0], brand=c[1])[0])
    # print(list_Products)
    # res = []
    # [res.append(x) for x in list_Products if x.category not in res.category]
    #####################

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

        if 'brandsCategories' in request.POST and len(request.POST.getlist('brandsCategories', [])) >= 1:

            brandsLstCat = request.POST.getlist('brandsCategories', [])

            categories = request.POST.getlist('categories', [])
            print(categories)

            for cat in categories:
                for brandCat in brandsLstCat:
                    productS = Product.objects.filter(brand__icontains=brandCat, category__icontains=cat)

                    if len(productS) >= 1:
                        for p in productS:
                            productsList.append(p)
                result = productsList


        if 'brandsProducts' in request.POST:
            brandsLst = request.POST.getlist('brandsProducts', [])
            for brand in brandsLst:
                if brand != '':
                    products = Product.objects.filter(
                        brand=brand)
                    if len(products) >= 1:
                        for p in products:
                            productsList.append(p)
                    else:
                        productsList = result
            result = productsList

        if 'priceRange' in request.POST:
            minPrice = request.POST['minPrice']
            maxPrice = request.POST['maxPrice']
            result = Product.objects.filter(price__range=[minPrice, maxPrice])

    tparams = {'productsFilter': productsFilter,
               'totalBrands': Product.objects.values('brand').distinct().count(),
               'totalCategories': Product.objects.values('category').distinct().count(),
               'brands': brands,
               'productsList': result,

               }
    return render(request, 'shop.html', tparams)


def home(request):
    assert isinstance(request, HttpRequest)
    recommendedProducts = Product.objects.all()[0:3]
    comments = Comment.objects.order_by('userEmail').distinct()

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(userName=form.cleaned_data["userName"],
                              userEmail=form.cleaned_data["userEmail"],
                              description=form.cleaned_data["description"],
                              rating=form.cleaned_data["rating"],
                              commentDate=form.cleaned_data["commentDate"],
                              )
            comment.save()
            return redirect("home")
    else:
        form = CommentForm()
    return render(request, 'index.html',
                  {"form": form, "recommendedProducts": recommendedProducts, "comments": comments})


def account(request):
    shoppingCarts = ShoppingCart.objects.filter(user_id=request.user.id)
    if shoppingCarts:
        assoc = []
        for scs in shoppingCarts:
            scis = ShoppingCartItem.objects.filter(cart_id=scs.id)
            payment = Payment.objects.filter(shopping_cart=scs)[0]
            print(payment.total)
            assoc.append((scis, payment))
        tparams = {'carts': assoc}

    else:
        tparams = {'cart': []}
        shoppingCarts = []
    return render(request, 'account.html', tparams)


def checkout(request):
    if request.user.is_authenticated:
        tparams = getShoppingCart(request)

        if request.method == 'POST':
            form = paymentForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                type = data['type']
                card_no = data['card_no']

                address = data['address']
                pm = PaymentMethod(type=type, card_no=card_no)
                pm.save()
                sp = ShoppingCart(user_id=request.user.id)
                sp.save()
                payment = Payment()
                payment.address = address
                payment.total = round(tparams['total'], 2)
                payment.method = pm
                payment.shopping_cart = sp
                payment.save()
                for item, quantity in tparams['cart']:
                    spi = ShoppingCartItem()
                    spi.product = item
                    item.quantity = item.quantity - spi.quantity
                    item.save()
                    if item.quantity == 0:
                        item.stock = False
                    spi.quantity = quantity
                    spi.cart_id = sp.id
                    spi.save()
                carts[request.user.id] = []
                return redirect('account')
        else:
            form = paymentForm()
        tparams['form'] = form

        return render(request, 'checkout.html', tparams)
    return redirect('login')


def getShoppingCart(request):
    userCart = []
    if request.user.id in carts:
        userCart = carts[request.user.id]
    currentCart = []
    total = 0
    totalDiscount = 0
    userCart.sort(key=lambda a: a[0])
    for item in userCart:
        product = Product.objects.get(id=item[0])
        currentCart.append((product, item[1]))
        total += product.price * item[1]

        if item[1] >= product.quantity:
            item[1] = product.quantity
        if product.promotion:
            totalDiscount += product.price * product.promotion.discount * item[1]
    tparams = {
        'cart': currentCart,
        'subtotal': round(total, 2),
        'discount': round(totalDiscount, 2),
        'total': round(total - totalDiscount, 2),
    }
    return tparams


def addToCart(request, id):
    if request.user.is_authenticated:
        if request.user.id in carts:
            products = [p for p in carts[request.user.id] if str(p[0]) != id]
            curProduct = [p for p in carts[request.user.id] if p not in products]
            if curProduct:
                prod = curProduct[0]
                prod = [id, prod[1] + 1]
                products.append(prod)
                carts[request.user.id] = products
            else:
                carts[request.user.id].append([id, 1])
        else:
            carts[request.user.id] = [[id, 1]]

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login')


def removeFromCart(request, id):
    if request.user.is_authenticated:
        if request.user.id in carts:
            products = [p for p in carts[request.user.id] if str(p[0]) != id]
            carts[request.user.id] = products
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login')


def increaseQuantity(request, id):
    if request.user.is_authenticated:
        products = [p for p in carts[request.user.id] if str(p[0]) != id]
        prod = [p for p in carts[request.user.id] if p not in products][0]
        prod = [id, prod[1] + 1]
        products.append(prod)
        carts[request.user.id] = products
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login')


def decreaseQuantity(request, id):
    if request.user.is_authenticated:
        products = [p for p in carts[request.user.id] if str(p[0]) != id]
        prod = [p for p in carts[request.user.id] if p not in products][0]
        prod = [id, prod[1] - 1]
        products.append(prod)
        carts[request.user.id] = products

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login')


def cart(request):
    if request.user.is_authenticated:
        tparams = getShoppingCart(request)
        return render(request, 'cart.html', tparams)
    return redirect('login')
