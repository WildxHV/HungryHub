from django.shortcuts import render

from vendor.models import Vendor


def home(request):
    vendors = Vendor.objects.filter(is_approved = True, user__is_active = True)[:8]
    context ={
        'vendors' : vendors,
    }
    return render(request, 'home.html',context)

def custom_error_404(request, exception):
    return render(request, 'error/404error.html', status=404)


def custom_error_500(request):
    return render(request, 'error/500error.html', status=500)