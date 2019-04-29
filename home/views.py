from django.shortcuts import render

# Create your views here.
def index(requset):
    return render(requset, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')
