from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def custom_error_404(request, exception):
    return render(request, 'error/404error.html', status=404)


def custom_error_500(request):
    return render(request, 'error/500error.html', status=500)