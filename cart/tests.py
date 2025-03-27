from django.test import TestCase
from django.utils import timezone
from carparts.models import Part, Category, Brand
from cart.models import Cart, CartItem
from django.urls import reverse

class CartModelsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        
        self.part = Part.objects.create(
            title='Test Part',
            price=70.0,
            stock=3,
            description='Test description'
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)
        
        self.cart = Cart.objects.create(cart_id='test_cart', date_added=timezone.now())
        self.cart_item = CartItem.objects.create(
            part=self.part,
            cart=self.cart,
            quantity=2,
            active=True
        )

    def test_cart_str_method(self):
        self.assertEqual(str(self.cart), 'test_cart')

    def test_cart_item_sub_total_method(self):
        expected_sub_total = self.part.price * self.cart_item.quantity
        self.assertEqual(self.cart_item.sub_total(), expected_sub_total)

    def test_cart_item_str_method(self):
        expected_str = self.part.title
        self.assertEqual(str(self.cart_item.part.title), expected_str)


class CartViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        
        self.part = Part.objects.create(
            title='Test Part',
            price=70.0,
            stock=3,
            description='Test description'
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)

    def test_add_cart(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.part.id]))
        self.assertEqual(response.status_code, 302)  # Redirect expected
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(part=self.part, cart=cart)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_cart_quantity_limit(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.part.id]))
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(part=self.part, cart=cart)
        self.assertEqual(cart_item.quantity, 1)
        
        # Attempt to add more items than available stock
        for _ in range(3):
            self.client.get(reverse('cart:add_cart', args=[self.part.id]))
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, self.part.stock)


class CartRemoveViewTest(TestCase):
    def setUp(self):
        # Create a category and brand for the part
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')

        # Create a part for testing
        self.part = Part.objects.create(
            title='Test Part',
            description='Test description',
            price=70.0,
            stock=3
        )
        self.part.category.add(self.category)
        self.part.brand.add(self.brand)

    def _cart_id(self, request):
        return request.session.session_key

    def test_cart_remove_view(self):
        # Set up a request with a session
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        # Set the cart ID using the _cart_id function
        request.session['cart_id'] = self._cart_id(request)

        # Create a cart using the _cart_id function
        cart = Cart.objects.create(cart_id=request.session['cart_id'])
        cart_item = CartItem.objects.create(part=self.part, quantity=2, cart=cart)

        # Make a request to the cart_remove view
        response = self.client.post(reverse('cart:cart_remove', args=[self.part.id]))

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the cart_item quantity is reduced by 1
        updated_cart_item = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated_cart_item.quantity, 1)

    def test_cart_full_remove_view(self):
        # Set up a request with a session
        request = self.client.request().wsgi_request
        request.session = self.client.session
        request.session.save()

        # Set the cart ID using the _cart_id function
        request.session['cart_id'] = self._cart_id(request)

        # Create a cart using the _cart_id function
        cart = Cart.objects.create(cart_id=request.session['cart_id'])
        cart_item = CartItem.objects.create(part=self.part, quantity=1, cart=cart)

        # Make a request to the full_remove view for the last item
        response = self.client.post(reverse('cart:full_remove', args=[self.part.id]))

        # Assert that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the cart_item is deleted
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=cart_item.id)