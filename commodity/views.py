from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.models import User

import sys
sys.path.append('..')
from users.models import Message, UserInfo
from AntMark import settings

from .models import CommodityTag, Commodity, CommoditySource
from .forms import CommodityTagForm, CommodityForm, CommoditySourceForm
from helper.decorator import user_verify_required


# 显示所有商品标签，暂无作用
def tag_list(request):
    tags = CommodityTag.objects.all()
    context = {'tags':tags}
    return render(request, 'commodity/common/tag_list.html', context)

# 显示所有商品货源，暂无作用
def source_list(request):
    sources = CommoditySource.objects.all()
    context = {'sources':sources}
    return render(request, 'commodity/common/source_list.html', context)

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
    context = {'commodities':commodities, 'page':current_page}
    return render(request, 'commodity/common/commodity_list.html', context)

# 显示商品详情
@login_required(login_url = '/users/login')
@csrf_exempt
def commodity_detail(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    if commodity.is_verified and commodity.for_sale :
        # commodity_tags_ids = commodity.commodity_tag.values_list("id", flat = True)
        # similar_commodities = Commodity.objects.filter(commodity_tag__in = commodity_tags_ids).exclude(id = commodity.id)
        similar_commodities = Commodity.objects.filter(commodity_tag = commodity.commodity_tag).exclude(id = commodity.id)
        similar_commodities = similar_commodities[:4]
        context = {"commodity":commodity, "similar_commodities":similar_commodities}
        return render(request, "commodity/common/commodity_detail.html", context)
    else:
        return HttpResponse("404")


# 个人商品库
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def commodity_repertory(request):
    commodity_list = Commodity.objects.filter(owner = request.user)
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
    context = {'commodities':commodities, 'page':current_page}
    return render(request, 'commodity/personal/commodity_repertory.html', context)

# 创建商品
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def create_commodity(request):
    if request.method == 'POST':
        commodity_form = CommodityForm(data = request.POST)
        if commodity_form.is_valid():
            cd = commodity_form.cleaned_data
            try:
                tag = CommodityTag.objects.get(tag = request.POST['tag'])
                source = CommoditySource.objects.get(source = request.POST['source'])
                commodity = Commodity.objects.create(owner=request.user, commodity_source = source, commodity_tag = tag)
                
                commodity.title = cd['title']
                commodity.body = cd['body']
                commodity.price = cd['price']
                commodity.for_sale = False
                commodity.is_verified = False
                commodity.save()
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
        context = {'commodity_form':commodity_form, 'tags':tags, 'sources':sources}
        return render(request, 'commodity/personal/create_commodity.html', context)


# 编辑商品信息
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def edit_commodity(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    if request.method == 'GET':
        commodity_form = CommodityForm()
        sources = CommoditySource.objects.all()
        tags = CommodityTag.objects.all()
        context = {'commodity':commodity, 'commodity_form':commodity_form, 'sources':sources, 'tags':tags}
        return render(request, 'commodity/personal/edit_commodity.html', context)
    else:
        commodity_form = CommodityForm(data = request.POST)
        if commodity_form.is_valid():
            cd = commodity_form.cleaned_data
            try:
                tag = CommodityTag.objects.get(tag = request.POST['tag'])
                source = CommoditySource.objects.get(source = request.POST['source'])
                commodity.title = cd['title']
                commodity.price = cd['price']
                commodity.body = cd['body']
                commodity.commodity_tag = tag
                commodity.commodity_source =  source
                commodity.is_verified = False
                commodity.for_sale = False

                commodity.save()
                return HttpResponseRedirect(reverse('commodity:not_verified_list'))
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")

# 上传商品图像
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def commodity_image(request, id):
    if request.method == 'POST':
        img = request.POST['img']
        commodity = Commodity.objects.get(id=id) 
        commodity.image = img
        commodity.save()
        return HttpResponse("1")
    else:
        context = {'id':id}
        return render(request, 'commodity/personal/imagecrop.html', context)

# 删除商品
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
@user_verify_required
def del_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 预览商品
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def preview_commodity(request, id):
    commodity = get_object_or_404(Commodity, id = id)
    # commodity_tags_ids = commodity.commodity_tag.values_list("id", flat = True)
    context = {"commodity":commodity}
    return render(request, "commodity/personal/preview_commodity.html", context)


# 待上架的商品列表
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def put_on_shelves_list(request):
    commodity_list = Commodity.objects.filter(owner = request.user, for_sale = False, is_verified = True)
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
    context = {'commodities':commodities, 'page':current_page}
    return render(request, 'commodity/personal/put_on_shelves_list.html', context)

# 将商品库的商品上架
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
@user_verify_required
def put_on_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.for_sale = True
        commodity.save()
        return HttpResponse("1")
    except:
        return HttpResponse('2')

# 正在上架的商品列表
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def put_off_shelves_list(request):
    commodity_list = Commodity.objects.filter(owner = request.user, for_sale = True, is_verified = True)
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
    context = {'commodities':commodities, 'page':current_page}
    return render(request, 'commodity/personal/put_off_shelves_list.html', context)

# 将商品下架
@login_required(login_url = '/users/login')
@require_POST
@csrf_exempt
@user_verify_required
def put_off_commodity(request):
    commodity_id = request.POST['commodity_id']
    try:
        commodity = Commodity.objects.get(id = commodity_id)
        commodity.for_sale = False
        commodity.save()
        return HttpResponse("1")
    except:
        return HttpResponse('2')

# 未通过审核商品列表
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def not_verified_list(request):
    commodity_list = Commodity.objects.filter(owner = request.user, is_verified = False)
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
    context = {'commodities':commodities, 'page':current_page}
    return render(request, 'commodity/personal/not_verified_list.html', context)  

# 提出商品审核
@login_required(login_url = '/users/login')
@csrf_exempt
@user_verify_required
def commodity_verify(request, comm_id):
    commodity = Commodity.objects.get(id = comm_id)
    info = UserInfo.objects.get(user = request.user)
    text = "用户" + info.nickname + "(" + request.user.username + ")" + \
            "提交了商品身份认证文件，请点击以下链接进行审核：" + "<a href=" + settings.CUR_HOST + \
            "/admin_manage/comm_verfity/" + str(commodity.id) + ">审核链接</a>"
    admin_user = User.objects.filter(is_superuser=True)[0]
    Message.objects.create(text = text, id_content=comm_id, msg_type='commodity_verify', 
        sender=request.user, receiver = admin_user)
    response_data = {
        'message': "商品已经提交审核，等待管理员通知",
        'next_page': "商品提交审核页面",
        'goto_url': settings.CUR_HOST + 'commodity/not-verified-list/',
        'goto_time': 3,
    }
    return render(request, 'users/notice.html' , response_data)


# 搜索和筛选商品
@login_required(login_url = "/users/login")
@csrf_exempt
def search_commodity(request):
    keyword = request.POST.get('keyword')
    if keyword != "":
        condition = {}
        tagChoice = request.POST.get('tag', None)
        if tagChoice is not None and tagChoice != "0":
            tag = CommodityTag.objects.get(tag = tagChoice)
            condition['commodity_tag'] = tag.id
        
        sourceChoice = request.POST.get('source', None)
        if sourceChoice is not None and sourceChoice != "0": 
            source = CommoditySource.objects.get(source = sourceChoice)
            condition['commodity_source'] = source.id
        commodity_list = Commodity.objects.filter(title__icontains = keyword, **condition)
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
        context = {'commodities':commodities, 'keyword':keyword, 'page':current_page, 'tags':tags, 'sources':sources}
        return render(request, 'commodity/common/search_commodity.html', context)    
    else:
        return HttpResponseRedirect(reverse('commodity:commodity_list'))    
