from django.shortcuts import render, redirect
from .models import Grocerystore, Userpaymentinfo, Address, Deliverydriver, Grocerystoreadd, Groceryitem, Purchaseinfo, PurchaseinfoHasGroceryitem, Orderstatus
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, addAddressForm, addPaymentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime
from django.utils import timezone

@login_required(login_url='loginPage') # only logged in users can see this page
def index(request):
    all_stores = Grocerystore.objects.all
    all_payinfo = Userpaymentinfo.objects.all
    all_addresses = Address.objects.all
    all_drivers = Deliverydriver.objects.all
    all_grocstoreaddresses = Grocerystoreadd.objects.all
    all_groceryitem = Groceryitem.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/index.html', {'stores':all_stores, 'paymentInfo':all_payinfo, 'addresses':all_addresses,'drivers':all_drivers,'groceryaddresses':all_grocstoreaddresses, 'groceryitem': all_groceryitem, 'numberItems':numberItems }) # cart items for only the user

@login_required(login_url='loginPage') # only logged in users can see this page
def vons(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/vons.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def vonsAddCart(request, item_id):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/vons.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def vonsSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/vons.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/vons.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def vonsCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/vons.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})

@login_required(login_url='loginPage') # only logged in users can see this page
def smart_final(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/smart&final.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def smart_finalSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/smart&final.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/smart&final.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def smartCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/smart&final.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def smart_finalAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/smart&final.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
@login_required(login_url='loginPage') # only logged in users can see this page
def wholefoods(request):
    all_stores = Grocerystore.objects.all
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/wholefoods.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def wholefoodsSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/wholefoods.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/wholefoods.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def wholefoodsCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/wholefoods.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def wholefoodsAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/wholefoods.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})

@login_required(login_url='loginPage') # only logged in users can see this page
def traderjoes(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/traderjoes.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def traderjoesSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all()
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/traderjoes.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/traderjoes.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def traderjoesCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/traderjoes.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def traderjoesAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/traderjoes.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
@login_required(login_url='loginPage') # only logged in users can see this page
def food4less(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/food4less.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def food4lessSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/food4less.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/food4less.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def food4lessCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/food4less.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def food4lessAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/food4less.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})

@login_required(login_url='loginPage') # only logged in users can see this page
def ralphs(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/ralphs.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def ralphsSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/ralphs.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/ralphs.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def ralphsCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/ralphs.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def ralphsAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/ralphs.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})

@login_required(login_url='loginPage') # only logged in users can see this page
def staterbros(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/staterbros.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def staterbrosSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/staterbros.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/staterbros.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def staterbrosCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/staterbros.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def staterbrosAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/staterbros.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
@login_required(login_url='loginPage') # only logged in users can see this page
def elsuper(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/elsuper.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def elsuperSearch(request):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    if request.method == "POST":
        searchkey = request.POST['searchkey']
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.filter(groceryname__icontains = searchkey)
        return render(request, 'hello/elsuper.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
    else: 
        all_stores = Grocerystore.objects.all
        all_items = Groceryitem.objects.all
        return render(request, 'hello/elsuper.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def elsuperCats(request, cats):
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.filter(category = cats)
    all_itemss = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_itemss:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/elsuper.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
def elsuperAddCart(request, item_id):
    print("addtocart")
    all_stores = Grocerystore.objects.all
    all_items = Groceryitem.objects.all()
    product = Groceryitem.objects.get(groceryid = item_id)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user)
    store = product.grocerystore_storeid # for mysql you have to create many to many with a connecting table
    user_order, status = Purchaseinfo.objects.get_or_create(grocerystore_storeid=store, auth_user = request.user, purchased = 0) # to track the items in the order
    order_item, status = PurchaseinfoHasGroceryitem.objects.get_or_create(purchaseinfo_purchaseid = user_order, groceryitem_groceryid = product) # purchaseinfo will have its id and the id of the orderitem #inside this new table, this is where the purchase info will have its list of items through the connecting table
    if status: 
        user_order.save()
        order_item.save()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    return render(request, 'hello/elsuper.html', {'stores':all_stores, 'items':all_items, 'numberItems':numberItems})
@login_required(login_url='loginPage') # only logged in users can see this page
def cart(request):
    context = {}
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    totalPrice = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    for i in user_orders:
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        totalPrice = totalPrice + m.getPrice()
    print(totalPrice)
    context['user_orders'] = user_orders
    context['all_items'] = all_items
    context['all_orderitems'] = all_orderitems
    context['numberItems'] = numberItems
    context['totalPrice'] = totalPrice
    return render(request, 'hello/cart.html',context)

@login_required(login_url='loginPage') # only logged in users can see this page
def checkout(request): # choose address and payment option show total price
    context = {}
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    addresses = Address.objects.filter(auth_user = request.user)
    payments = Userpaymentinfo.objects.filter(auth_user = request.user)
    totalPrice = 0
    for i in user_orders:
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        totalPrice = totalPrice + m.getPrice()
    context['all_orderitems'] = all_orderitems
    context['user_orders'] = user_orders
    context['all_items'] = all_items
    context['numberItems'] = numberItems
    context['totalPrice'] = totalPrice
    context['addresses'] = addresses
    context['payments'] = payments
    return render(request, 'hello/checkout.html', context)

@login_required(login_url='loginPage') # only logged in users can see this page
def payment(request, address): # chosen address and now prompt user for payment 
    context = {}
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    addresses = Address.objects.filter(auth_user = request.user)
    payments = Userpaymentinfo.objects.filter(auth_user = request.user)
    totalPrice = 0
    user_order = Purchaseinfo.objects.get(auth_user = request.user, purchased = 0)
    user_address = Address.objects.get(useraddressid=address)
    user_order.address_useraddressid = user_address
    for i in user_orders:
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        totalPrice = totalPrice + m.getPrice()
    context['totalPrice'] = totalPrice
    context['all_orderitems'] = all_orderitems
    context['all_items'] = all_items
    context['user_orders'] = user_orders
    context['user_order'] = user_order
    context['numberItems'] = numberItems
    context['payments'] = payments
    context['user_address'] = user_address
    user_order.save()
    return render(request, 'hello/payment.html', context)

@login_required(login_url='loginPage') # only logged in users can see this page
def confirmation(request, payment):
    context = {}
    all_items = Groceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    order_payment = Userpaymentinfo.objects.get(paymentid=payment)
    totalPrice = 0
    user_order = Purchaseinfo.objects.get(auth_user = request.user, purchased =0 )
    user_address = user_order.address_useraddressid
    user_order.userpaymentinfo_paymentid = order_payment
    for i in user_orders:
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        totalPrice = totalPrice + m.getPrice()
    context['totalPrice'] = totalPrice
    context['all_orderitems'] = all_orderitems
    context['all_items'] = all_items
    context['user_orders'] = user_orders
    context['user_order'] = user_order
    context['numberItems'] = numberItems
    context['user_address'] = user_address
    context['order_payment'] = order_payment
    user_order.save()
    return render(request, 'hello/confirmation.html', context)
    
def orderconfirmed(request, order):
    context = {}
    all_items = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    user_order = Purchaseinfo.objects.get(purchaseid=order)
    user_address = user_order.address_useraddressid
    order_payment = user_order.userpaymentinfo_paymentid
    totalPrice = 0
    totalItems = 0
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    for j in all_orderitems:
            if user_order.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        totalItems = totalItems + 1
                        totalPrice = totalPrice + m.getPrice()
    orderstatus, status = Orderstatus.objects.get_or_create(purchaseinfo_purchaseid=user_order, ordertime=timezone.now(), archive = 0)
    if status: 
        orderstatus.save()
    user_order.totalprice = totalPrice
    user_order.totalitems = totalItems
    user_order.datetime = timezone.now()
    user_order.purchased = 1
    context['all_orderitems'] = all_orderitems
    context['all_items'] = all_items
    context['totalPrice'] = totalPrice
    context['user_order'] = user_order
    context['user_orders'] = user_orders
    context['user_address'] = user_address
    context['numberItems'] = numberItems
    context['order_payment'] = order_payment
    user_order.save()
    return render(request,'hello/orderconfirmed.html', context)

def orders(request):
    context = {}
    all_items = Groceryitem.objects.all()
    all_orderitems = PurchaseinfoHasGroceryitem.objects.all()
    user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 0)
    all_user_orders = Purchaseinfo.objects.filter(auth_user = request.user, purchased = 1)
    order_statuses = Orderstatus.objects.all()
    unarchived_statuses = Orderstatus.objects.filter(archive = 0)
    current_time = timezone.now()
    numberItems = 0
    for i in user_orders: # number of items in cart for user
        for j in all_orderitems:
            if i.getPurchaseID() is j.getPurchaseID():
                for m in all_items:
                    if j.getGroceryID() is m.getGroceryID():
                        numberItems = numberItems + 1
    for i in unarchived_statuses:
        time = timezone.now() - i.ordertime
        print(time.seconds)
        minutes = (time.seconds//60)%60
        print(minutes)
        if (minutes < 3): # here is where the order statuses will be determined if not already
            i.status = "Order Processing"
            print("order processing")
        if ((minutes < 6) and (minutes > 3)):
            i.status = "Order in Progress"
            print("order in progress")
        if ((minutes < 25) and (minutes > 6)):
            i.status = "Order in Delivery"
            print("order in delivery")
        if ((minutes >= 25)):
            i.status = "Order Delivered"
            i.archive = 1
            print("order delivered") # also change the order status to archived
        i.save()
    context['numberItems'] = numberItems
    context['user_orders'] = user_orders
    context['all_user_orders'] = all_user_orders
    context['order_statuses'] = order_statuses
    context['current_time'] = current_time
    return render(request,'hello/orders.html', context)

@login_required(login_url='loginPage') # only logged in users can see this page
def userprofile(request):
    context = {}
    addresses = Address.objects.filter(auth_user = request.user)
    payments = Userpaymentinfo.objects.filter(auth_user = request.user)
    context ['addresses'] = addresses
    context ['payments'] = payments
    if request.method == "POST":
        if request.POST.get('streetaddress'):
            form = addAddressForm(request.POST or None)
            if form.is_valid():
                print ("valid")
                userid = request.user.id
                userobj = User.objects.get(id = userid)
                instance = form.save(commit = False)
                instance.auth_user = userobj
                instance.save()
                return render(request, 'hello/userprofile.html', context)
            else:
                context = {'form':form}
                return render(request, 'hello/userprofile.html', context)
        if request.POST.get('cardnumber'):
            form = addPaymentForm(request.POST or None)
            print("here")

            if form.is_valid():
                print("valid")
                userid = request.user.id
                userobj = User.objects.get(id = userid)
                instance = form.save(commit = False)
                instance.auth_user = userobj
                instance.save()
                return render(request, 'hello/userprofile.html', context)
            else:
                context = {'form':form}
                return render(request, 'hello/userprofile.html', context)
    else: 
        return render(request, 'hello/userprofile.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username') # createa variable
                messages.success(request, 'Account created for ' + user)
                return redirect('loginPage')
        context = {'form': form}
        return render(request, 'hello/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'hello/login.html', context)
# Create your views here.,
