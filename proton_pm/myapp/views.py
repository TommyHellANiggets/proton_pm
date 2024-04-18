from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def home(request):
    return render(request, 'main.html')

def terminal(request):
    return render(request, 'terminal.html')

def load_photo(request):
    return render(request, 'load_photo.html')

def profile(request):
    return render(request, 'profile.html')