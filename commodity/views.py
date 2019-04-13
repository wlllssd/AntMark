from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .models import CommodityTag, Commodity
from .forms import CommodityTagForm, CommodityForm

def tag_list(request):
    tags = CommodityTag.objects.all()
    return render(request, 'commodity/common/tag_list.html', {'tags':tags})

@login_required(login_url = '/users/login')
@csrf_exempt
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
    return render(request, 'commodity/common/commodity_list.html', {'commodities':commodities, 'page':current_page})

@login_required(login_url = '/users/login')
@csrf_exempt
def commodity_detail(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    return render(request, "commodity/common/commodity_detail.html", {"commodity":commodity})


@login_required(login_url = '/users/login')
@csrf_exempt
def commodity_repertory(request):
    commodity_list = Commodity.objects.filter(author = request.user)
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
    return render(request, 'commodity/personal/commodity_repertory.html', {'commodities':commodities, 'page':current_page})

@login_required(login_url = '/users/login')
@csrf_exempt
def edit_commodity(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    if request.method == 'GET':
        commodity_form = CommodityForm(initial = {'title':commodity.title, 'tags':commodity.commodity_tag, 'image':commodity.image})
        return render(request, 'commodity/personal/edit_commodity.html', {'commodity':commodity, 'commodity_form':commodity_form})
    else:
        try:
            commodity.amount = request.POST['amount']
            commodity.body = request.POST['body']
            commodity.price = request.POST['price']
            commodity.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")
        
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
def del_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url = '/users/login')
@csrf_exempt
def create_commodity(request):
    if request.method == 'POST':
        commodity_form = CommodityForm(data = request.POST)
        if commodity_form.is_valid():
            cd = commodity_form.cleaned_data
            try:
                new_commodity = commodity_form.save(commit = False)
                new_commodity.author = request.user
                new_commodity.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        commodity_form = CommodityForm()
        tags = CommodityTag.objects.all()
        return render(request, 'commodity/personal/create_commodity.html', {'commodity_form':commodity_form, 'tags':tags})


@login_required(login_url = '/users/login')
@csrf_exempt
def put_on_shelves_list(request):
    commodity_list = Commodity.objects.filter(author = request.user, for_sale = False)
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
    return render(request, 'commodity/personal/put_on_shelves_list.html', {'commodities':commodities, 'page':current_page})

@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
def put_on_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.put_on()
        return HttpResponse("1")
    except:
        return HttpResponse('2')

@login_required(login_url = '/users/login')
@csrf_exempt
def put_off_shelves_list(request):
    commodity_list = Commodity.objects.filter(author = request.user, for_sale = True)
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
    return render(request, 'commodity/personal/put_off_shelves_list.html', {'commodities':commodities, 'page':current_page})

@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
def put_off_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.put_off()
        return HttpResponse("1")
    except:
        return HttpResponse('2')
