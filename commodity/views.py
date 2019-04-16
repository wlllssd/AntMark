from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import CommodityTag, Commodity, CommoditySource
from .forms import CommodityTagForm, CommodityForm, CommoditySourceForm

# 显示所有商品标签，暂无作用
def tag_list(request):
    tags = CommodityTag.objects.all()
    return render(request, 'commodity/common/tag_list.html', {'tags':tags})

def source_list(request):
    sources = CommoditySource.objects.all()
    return render(request, 'commodity/common/source_list.html', {'sources':sources})

# 显示所有商品
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
    tags = CommodityTag.objects.all()
    sources = CommoditySource.objects.all()   
    return render(request, 'commodity/common/commodity_list.html', {'commodities':commodities, 'page':current_page, 'tags':tags, 'sources':sources})

# 显示商品详情
@login_required(login_url = '/users/login')
@csrf_exempt
def commodity_detail(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    return render(request, "commodity/common/commodity_detail.html", {"commodity":commodity})

# 个人商品库
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

# 创建商品
@login_required(login_url = '/users/login')
@csrf_exempt
def create_commodity(request):
    if request.method == 'POST':
        commodity_form = CommodityForm(data = request.POST)
        if commodity_form.is_valid():
            cd = commodity_form.cleaned_data
            try:
                commodity = Commodity.objects.create(author=request.user)
                commodity.title = cd['title']
                commodity.body = cd['body']
                
                # 获取商品标签（多对多）
                tagList = request.POST.getlist('tag', None)
                tags = CommodityTag.objects.filter(tag__in = tagList)
                commodity.commodity_tag.set(tags)

                # 获取商品货源（多对多）
                sourceList = request.POST.getlist('source', None)
                sources = CommoditySource.objects.filter(source__in = sourceList)
                commodity.commodity_source.set(sources)

                commodity.price = cd['price']
                commodity.amount = cd['amount']
                commodity.for_sale = False
                commodity.image = request.FILES.get('image', None)
                commodity.save()
                print("1")
                # 重定向
                return HttpResponseRedirect(reverse('commodity:commodity_repertory'))
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        commodity_form = CommodityForm()
        tags = CommodityTag.objects.all()
        sources = CommoditySource.objects.all()
        return render(request, 'commodity/personal/create_commodity.html', {'commodity_form':commodity_form, 'tags':tags, 'sources':sources})

# 编辑商品信息
@login_required(login_url = '/users/login')
@csrf_exempt
def edit_commodity(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    if request.method == 'GET':
        commodity_form = CommodityForm()
        sources = CommoditySource.objects.all()
        return render(request, 'commodity/personal/edit_commodity.html', {'commodity':commodity, 'commodity_form':commodity_form, 'sources':sources})
    else:
        commodity_form = CommodityForm(data = request.POST)
        if commodity_form.is_valid():
            cd = commodity_form.cleaned_data
            try:
                commodity.amount = cd['amount']
                commodity.price = cd['price']
                commodity.body = cd['body']

                # 获取商品货源（多对多）
                sourceList = request.POST.getlist('source', None)
                sources = CommoditySource.objects.filter(source__in = sourceList)
                commodity.commodity_source.set(sources)

                commodity.save()
                return HttpResponseRedirect(reverse('commodity:commodity_repertory'))
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")

# 删除商品
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

# 待上架的商品列表
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

# 将商品库的商品上架
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
def put_on_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.for_sale = True
        commodity.amount = 1
        commodity.save()
        return HttpResponse("1")
    except:
        return HttpResponse('2')

# 正在上架的商品列表
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

# 将商品下架
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
def put_off_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.for_sale = False
        commodity.amount = 0
        commodity.save()
        return HttpResponse("1")
    except:
        return HttpResponse('2')


# 搜索商品
@login_required(login_url = '/users/login')
@csrf_exempt
def search_commodity(request):
    keyword = request.POST.get('keyword')
    if keyword != "":
        commodity_list = Commodity.objects.filter(title__icontains = keyword)
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
        return render(request, 'commodity/common/search_commodity.html', {'commodities':commodities, 'page':current_page})    
    else:
        return HttpResponseRedirect(reverse('commodity:commodity_list'))

# 筛选商品
@login_required(login_url = "/users/login")
@csrf_exempt
def commodity_filter(request):
    pass
