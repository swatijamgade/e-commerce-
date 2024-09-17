from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from .models import Cart as CartModel
from products.reccomender import Recommender


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_product(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        # saving to db
        # user_cart, is_created = CartModel.objects.get_or_create(user=request.user)
        # user_cart.products.add(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    # update db
    # user_cart = CartModel.objects.get(user=request.user)
    # user_cart.products.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    for item in cart_items:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})

    r = Recommender()
    cart_products = [item['product'] for item in cart_items]

    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return render(request, 'cart/detail.html', {'cart': cart, 'recommended_products': recommended_products})


def test_session(request):
    """
    This view is just to understand the working of django session object
    :param request:
    :return:
    """
    # session is attribute of request
    print(dir(request.session))
    print(request.session)

    # accessing data from session
    num_views = request.session.get("num_visit", 0)

    # storing data in session
    request.session["num_visit"] = num_views + 1

    # force django to update session
    request.session.modified = True

    # testing browser cookie
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()

    response = render(request, 'cart/test.html', {"visits": num_views})
    response.set_cookie("key", "value")
    response.set_cookie("name", "anurag")
    response.set_cookie("course", "django")

    return response