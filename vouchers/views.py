from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Voucher 
from .forms import VoucherApplyForm

from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Voucher 
from .forms import VoucherApplyForm


from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Voucher 
from .forms import VoucherApplyForm

def voucher_apply(request):
    now = timezone.now()
    form = VoucherApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code'].strip()  # Remove whitespace from input
        if code:  # Check if any voucher was entered
            try:
                voucher = Voucher.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True
                )
                request.session['voucher_id'] = voucher.id
                request.session['invalid_voucher'] = False  # Valid voucher, reset invalid flag
            except Voucher.DoesNotExist:
                request.session['voucher_id'] = None
                request.session['invalid_voucher'] = True  # Invalid voucher entered
        else:
            request.session['voucher_id'] = None
            request.session['invalid_voucher'] = None  # No voucher entered
    else:
        request.session['voucher_id'] = None
        request.session['invalid_voucher'] = None  # No voucher entered

    return redirect('cart:cart_detail')




# Create your views here.
