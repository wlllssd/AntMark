from django.shortcuts import render
from admin_manage.models import Announcement

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def annos(request):
    """ 查看公告 """
    annos = Announcement.objects.all()[:5]
    context = { 'annos': annos }
    return render(request, 'home/annos.html', context)
