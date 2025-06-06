from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Voucher 
from .forms import VoucherApplyForm

def voucher_apply(request):
    now = timezone.now()
    form = VoucherApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code'].strip()  
        if code:  
            try:
                voucher = Voucher.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True
                )
                request.session['voucher_id'] = voucher.id
                request.session['invalid_voucher'] = False  
            except Voucher.DoesNotExist:
                request.session['voucher_id'] = None
                request.session['invalid_voucher'] = True  
        else:
            request.session['voucher_id'] = None
            request.session['invalid_voucher'] = None  
    else:
        request.session['voucher_id'] = None
        request.session['invalid_voucher'] = None  

    return redirect('cart:cart_detail')




# Create your views here.
