from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import json

# Create your views here.
def store(request):
     if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_number_item()
     else:
        items = []
        order = {'get_number_item': 0, 'get_total_price_item': 0,'shipping':False}
        cartItems = order['get_cart_items']
     products = Product.objects.all()
     context = {
        "products" : products,
         "cartItems":cartItems,

     }
     return render(request, 'store/store.html', context)

def cart(request):
     if request.user.is_authenticated:
         customer = request.user.customer
         order,created = Order.objects.get_or_create(customer=customer,complete = False)
         items = order.orderitem_set.all()
         cartItems = order.get_number_item()
     else:
        items = []
        order = {'get_number_item':0,'get_total_price_item':0,'shipping':False}
        cartItems = order['get_cart_items']
     context = {
         'items':items,
         'order' : order,
         "cartItems": cartItems,
     }
     return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_number_item': 0, 'get_total_price_item': 0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == "add":
        orderItem.quatity =(orderItem.quatity+1)
    elif action == "remove":
        orderItem.quatity = orderItem.quatity-1
    orderItem.save()

    if(orderItem.quatity) <= 0:
        orderItem.delete()

    return JsonResponse("Item was  added", safe=False)