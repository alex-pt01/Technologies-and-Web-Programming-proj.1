from django.db import models


# Create your models here.
class Promotion(models.Model):
    name = models.CharField(max_length=80)
    discount = models.FloatField(null=True)
    description = models.CharField(max_length=300)
    deadline = models.DateField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80)
    price = models.FloatField()
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='static/images')
    quantity = models.IntegerField()
    stock = models.BooleanField()
    brand = models.CharField(max_length=80)
    CATEGORY = (('Smartphones', 'Smartphones'),
                ('Computers', 'Computers'),
                ('Tablets', 'Tablets'),
                ('Drones', 'Drones')
                , ('Televisions', 'Televisions'))
    category = models.CharField(max_length=150, choices=CATEGORY)
    promotion = models.ForeignKey(Promotion, default=None, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comments(models.Model):
    userName = models.CharField(max_length=80)
    userEmail = models.EmailField()
    description = models.CharField(max_length=400)
    rating = models.IntegerField()

    def __str__(self):
        return self.userEmail





class PaymentMethod(models.Model):
    TYPES = (('Credit Card', 'Credit Card'), ('ATM', 'ATM'), ('Bank Transfer', 'Bank Transfer'), ('Paypal', 'Paypal'))
    type = models.CharField(choices=TYPES, max_length=150)
    card_no = models.CharField(max_length=12)


class ShoppingCart(models.Model):
    user_id = models.CharField
    date = models.DateField


class Payment(models.Model):
    address = models.CharField(max_length=250)
    total = models.FloatField(null=False)
    date = models.DateField()
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)


class ShoppingCartItem(models.Model):
    quantity = models.IntegerField(default=1)
    cart_id = models.CharField(null=False, max_length=150)
    item_id = models.ForeignKey(Product, on_delete=models.CASCADE)
