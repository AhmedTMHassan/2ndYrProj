from django.shortcuts import redirect, render, get_object_or_404
from carparts.models import Part
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from order.models import Order, OrderItem
from stripe import StripeError
from django.contrib import messages
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal
from django.core.mail import send_mail


import stripe

def place_order(request):
    """Place an order, update stock, and redirect to Stripe payment."""
   
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

   
    total = sum(item.part.price * item.quantity for item in cart_items)

   
    order = Order.objects.create(
        emailAddress=request.user.email,
        billingName=request.user.get_full_name(),
        total=total,  
    )

    
    for item in cart_items:
        part = item.part

        if item.quantity > part.stock:
            messages.error(request, f"Not enough stock for {part.title}.")
            return redirect('cart:cart_detail')

        
        OrderItem.objects.create(
            order=order,
            product=part.title,
            quantity=item.quantity,
            price=part.price,
        )

        
        part.stock -= item.quantity
        part.save()

    
    cart_items.delete()
    cart.delete()

    
    low_stock_parts = Part.objects.filter(stock__lt=3)  
    for part in low_stock_parts:
        try:
            send_mail(
                'Restock Alert',
                f'ALERT: The part "{part.title}" is low in stock (only {part.stock} left). Please restock ASAP.',
                'no-reply@onlineshop.com',
                ['admin@stock.local'],
                fail_silently=False,
                html_message=(
                    f"<p><strong>Restock Alert</strong></p>"
                    f"<p>Part: <strong>{part.title}</strong></p>"
                    f"<p>Remaining stock: {part.stock}</p>"
                    f"<p>Please restock this item immediately.</p>"
                )
            )
        except Exception as e:
            print(f"Failed to send email for {part.title}: {e}")

    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from AMO Car Parts',
                        },
                        'unit_amount': int(total * 100), 
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('order:thanks', args=[order.id])),
            cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"An error occurred while creating the Stripe session: {e}")
        return redirect('cart:cart_detail')

def resend_low_stock_alerts(request):
    parts = Part.objects.filter(stock__lt=3)
    if not parts.exists():
        messages.info(request, "No parts are currently below stock threshold.")
    for part in parts:
        send_mail(
            'Restock Alert',
            f'ALERT: "{part.title}" is low in stock (only {part.stock} left). Please restock ASAP.',
            'no-reply@onlineshop.com',
            ['admin@stock.local'],
            fail_silently=False,
            html_message=(
                f"<p><strong>Restock Alert</strong></p>"
                f"<p>Part: <strong>{part.title}</strong> (ID: {part.id})</p>"
                f"<p>Remaining stock: {part.stock}</p>"
            )
        )
    messages.success(request, f"Alerts sent for {parts.count()} part(s).")
    return redirect('cart:cart_detail')  



def _cart_id(request):
    """Retrieve or create a session cart ID."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, part_id):
    """Add a part to the cart."""
    part = get_object_or_404(Part, id=part_id)

    if part.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('carparts:part_detail', pk=part.id)

    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    cart_item, created = CartItem.objects.get_or_create(part=part, cart=cart)
    if not created and cart_item.quantity < part.stock:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display the cart details."""
    total = 0
    counter = 0
    discount = 0
    new_total = 0
    voucher = None
    stripe_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += cart_item.part.price * cart_item.quantity
            counter += cart_item.quantity

        voucher_id = request.session.get('voucher_id')
        if voucher_id:
            voucher = Voucher.objects.get(id=voucher_id)
            discount = total * (voucher.discount / Decimal('100'))
            new_total = total - discount
            stripe_total = int(new_total * 100)
        else:
            stripe_total = int(total * 100)

    except ObjectDoesNotExist:
        cart_items = []

    stripe.api_key = settings.STRIPE_SECRET_KEY
    description = 'Online Shop - New Order'
    voucher_apply_form = VoucherApplyForm()

    if request.method == 'POST':
        try:
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
                success_url=request.build_absolute_uri(
                    reverse('cart:new_order')
                ) + f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher_id}&cart_total={total}",
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'counter': counter,
                'error': str(e),
            })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'voucher_apply_form': voucher_apply_form,
        'new_total': new_total,
        'voucher': voucher,
        'discount': discount
    })


def cart_remove(request, part_id):
    """Remove one quantity of a part from the cart."""
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    part = get_object_or_404(Part, id=part_id)
    cart_item = get_object_or_404(CartItem, part=part, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_detail')


def full_remove(request, part_id):
    """Remove all quantities of a part from the cart."""
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    part = get_object_or_404(Part, id=part_id)
    cart_item = get_object_or_404(CartItem, part=part, cart=cart)
    cart_item.delete()

    return redirect('cart:cart_detail')


def empty_cart(request):
    """Empty the entire cart."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(cart=cart).delete()
        cart.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('carparts:part_list')


def create_order(request):
    """Create an order after successful payment."""
    try:
        session_id = request.GET.get('session_id')
        cart_total = request.GET.get('cart_total')
        voucher_id = request.GET.get('voucher_id')

        if not session_id:
            raise ValueError("Session ID not found.")

        session = stripe.checkout.Session.retrieve(session_id)
        customer_details = session.customer_details

        if not customer_details or not customer_details.address:
            raise ValueError("Missing information in the Stripe session.")

        order_details = Order.objects.create(
            token=session.id,
            total=session.amount_total / 100,
            emailAddress=customer_details.email,
            billingName=customer_details.name,
            billingAddress1=customer_details.address.line1,
            billingCity=customer_details.address.city,
            billingPostcode=customer_details.address.postal_code,
            billingCountry=customer_details.address.country,
            shippingName=customer_details.name,
            shippingAddress1=customer_details.address.line1,
            shippingCity=customer_details.address.city,
            shippingPostcode=customer_details.address.postal_code,
            shippingCountry=customer_details.address.country,
        )

        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        voucher = None
        if voucher_id:
            try:
                voucher = Voucher.objects.get(id=voucher_id)
                order_details.voucher = voucher
                order_details.discount = Decimal(cart_total) * (voucher.discount / Decimal('100'))
                order_details.total = Decimal(cart_total) - order_details.discount
                order_details.save()
            except Voucher.DoesNotExist:
                pass

        for item in cart_items:
            OrderItem.objects.create(
                product=item.part.title,
                quantity=item.quantity,
                price=item.part.price,
                order=order_details
            )
            item.part.stock = max(0, item.part.stock - item.quantity)
            item.part.save()

        cart_items.delete()
        cart.delete()

        return redirect(reverse('order:thanks', args=[order_details.id]))

    except ValueError as ve:
        print(f"Error: {ve}")
        return redirect("carparts:part_list")

    except StripeError as se:
        print(f"Stripe Error: {se}")
        return redirect("carparts:part_list")

    except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect("carparts:part_list")