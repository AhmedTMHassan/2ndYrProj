from django.shortcuts import redirect, render, get_object_or_404
from carparts.models import Part
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, part_id):
    part = Part.objects.get(id=part_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist: 
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(part=part, cart=cart)
        if (cart_item.quantity < cart_item.part.stock):
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(part=part, quantity=1,cart=cart)
    return redirect('cart:cart_detail') 


def cart_detail(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.part.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)  # Convert total to cents
    description = 'Online Shop - New Order'
    

    if request.method == 'POST':
        try:
            # Create a new Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from AMO Car Parts',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
 		   billing_address_collection='required', 
                shipping_address_collection={},
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('carparts:part_list')), 
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),    
            )
            # Redirect to Stripe Checkout
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Render the template with an error message
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'counter': counter,
                'error': str(e),  # Display error if there's an issue with Stripe
            })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
    })


def cart_remove(request, part_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    part = get_object_or_404(Part, id=part_id)
    cart_item = CartItem.objects.get(part=part, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, part_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    part = get_object_or_404(Part, id=part_id)
    cart_item = CartItem.objects.get(part=part, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
