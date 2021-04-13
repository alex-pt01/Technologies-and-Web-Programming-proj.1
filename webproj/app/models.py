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
    image = models.ImageField(upload_to='static/portfolio')
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
