from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CommodityTag, Commodity
from .forms import CommodityTagForm, CommodityForm

def tag_list(request):
    tags = CommodityTag.objects.all()
    return render(request, 'commodity/tag_list.html', {'tags':tags})

@login_required(login_url = '/users/login')
def commodity_list(request):
    commodity_list = Commodity.objects.all()
    paginator = Paginator(commodity_list, 10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        commodities = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        commodities = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(1)
        commodities = current_page.object_list
    return render(request, 'commodity/commodity_list.html', {'commodities':commodities, 'page':current_page})

@login_required(login_url = '/users/login')
def commodity_detail(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    return render(request, "commodity/commodity_detail.html", {"commodity":commodity})
