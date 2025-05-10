from django.shortcuts import render

def home_view(request):
    return render(request, 'catalog/home.html')

def contacts_view(request):
    success = False
    if request.method == 'POST':
        message = request.POST.get('message')

        success = True
    return render(request, 'catalog/contacts.html', {'success': success})
