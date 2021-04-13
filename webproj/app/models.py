from django.db import models

# Create your models here.
class Promotion(models.Model):
    name = models.CharField(max_length=80)
    discount = models.FloatField(null=True)
    description = models.CharField(max_length=300)
    deadline = models.DateField()

class Product(models.Model):
    name = models.CharField(max_length=80)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=300)
    ranking = models.IntegerField()
    image = models.ImageField(upload_to='static/images')
    quantity = models.IntegerField()
    stock = models.BooleanField()
    brand = models.CharField(max_length=80)
    CATEGORY = (('Smartphones','Smartphones'),
                ('Computers','Computers'),
                ('Tablets','Tablets'),
                ('Drones','Drones')
                ,('Televisions','Televisions'))
    category = models.CharField(max_length= 150, choices = CATEGORY)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


