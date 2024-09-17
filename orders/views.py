from django.shortcuts import render
from django.shortcuts import redirect, reverse

from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created

from cart.cart import Cart
from cart.models import Cart as CartModel


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart.get_cart_items():
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # clear the cart
            cart.clear_cart()
            # # delete the cart from db
            # user_cart = CartModel.objects.get(user=request.user)
            # user_cart.products.clear()
            # user_cart.delete()
            # launch asynchronous task
            order_created.delay(order.id)
            print("mail sent successfully!")
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


def send_mail(request):
    pass