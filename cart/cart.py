from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:

    def __init__(self, request):
        """
        Initialize the cart.
        CART_SESSION_ID = 'cart'
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session if none exists
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        request.session['cart'] = {}
        request.session['cart'] = {12: {'quantity': 0, 'price': '10.00'}}
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # If product not in cart, initialize it with quantity and price
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            # Override the quantity if specified
            self.cart[product_id]['quantity'] = quantity
        else:
            # Otherwise, increase the quantity
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_cart_items(self):
        """
        Get all items in the cart with product details.
        """
        # get product ids from cart
        product_ids = self.cart.keys()
        # get the product from db based on ids
        products = Product.objects.filter(id__in=product_ids)
        # add product details to the cart
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        # calculate total price for each item
        cart_items = []
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            cart_items.append(item)
        return cart_items

    def remove_product(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Save the cart state to the session.
        """
        self.session.modified = True

    def clear_cart(self):
        """
        Clear the cart entirely.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calculate the total price of items in the cart.
        """
        total_price = Decimal('0.00')
        for item in self.cart.values():
            price = Decimal(item['price'])
            quantity = item['quantity']
            total_price += price * quantity
        return total_price