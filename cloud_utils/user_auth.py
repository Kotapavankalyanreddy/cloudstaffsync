from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def process_login(request, role):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return user
    return None
