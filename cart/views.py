from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from MainApp.models import Product, Category,Customer

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    customer = Customer.objects.get(pk=request.user.pk)
    customer_discount = round(cart.get_total_price() * ((customer.discount)/100))
    order_price = cart.get_total_price() - customer_discount
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'categories': categories,
                                                "order_price": order_price,
                                                "customer_discount": customer_discount})


