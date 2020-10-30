from django.db import models
from django.contrib.auth.models import  User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)

    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL,null=True,blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transactionID = models.CharField(max_length=200,null=True)

    @property

    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping = True
        return shipping

    def get_number_item(self):
        orderitem = self.orderitem_set.all()
        sum = 0;
        for item in orderitem:
            sum+= item.quatity;
        return sum;
    def get_total_price_item(self):
        orderItem = self.orderitem_set.all()
        sum = 0
        for item in orderItem:
            sum+=item.total_price()
        return sum

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quatity = models.PositiveIntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price*self.quatity

class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


