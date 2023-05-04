from django.shortcuts import render, redirect
from pypinyin import lazy_pinyin, Style
import requests
import parsel
from houseinfo import models
from django.utils.safestring import mark_safe

# Create your views here.


def get_first_letter(str1):
    ans = ''.join(lazy_pinyin(str1, style=Style.FIRST_LETTER))
    return ans


def pachong(py_name, page_num):
    res = []
    city_name = py_name
    page = int(page_num)
    for page in range(1, page + 1):
        url = "https://{0}.lianjia.com/ershoufang/pg{1}".format(city_name, page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.3161 SLBChan/25"
        }
        response = requests.get(url=url, headers=headers)
        response.close()
        selector = parsel.Selector(response.text)
        lis = selector.css('.sellListContent li')
        for li in lis:
            dit = {}
            positionInfo = li.css('.positionInfo a::text').getall()
            info = '-'.join(positionInfo)
            dit['builder'] = info
            houseInfo = li.css('.houseInfo::text').get()
            housrInfoSplit = houseInfo.split('|')
            if len(housrInfoSplit) == 7:
                dit['houseType'] = housrInfoSplit[0]
                dit['area'] = housrInfoSplit[1]
                dit['direction'] = housrInfoSplit[2]
                dit['decoration'] = housrInfoSplit[3]
                dit['floor'] = housrInfoSplit[4]
                dit['year'] = housrInfoSplit[5]
                dit['structure'] = housrInfoSplit[6]
            else:
                dit['houseType'] = housrInfoSplit[0]
                dit['area'] = housrInfoSplit[1]
                dit['direction'] = housrInfoSplit[2]
                dit['decoration'] = housrInfoSplit[3]
                dit['floor'] = housrInfoSplit[4]
                dit['year'] = '不详'
                dit['structure'] = housrInfoSplit[5]
            Price = li.css('.totalPrice span::text').get()
            dit['total_price'] = Price
            unitPrice = li.css('.unitPrice span::text').get()
            dit['unit_price'] = unitPrice
            res.append(dit)
    print("爬取成功！")
    return res


def mainscene(request):
    if request.method == 'GET':
        return render(request, "mainscene.html")
    else:
        global name
        name = request.POST.get("cityname")
        print(name)
        return redirect("/cityinfo/")
    

def cityinfo(request):
    if request.method == 'GET':
        return render(request, 'cityinfo.html', {"cityname": name})
    pagenum = request.POST.get("pagenum")
    if pagenum == 0:
        return redirect('/showdata/')
    else:
        print(pagenum)
        py_name = get_first_letter(name)
        print(py_name)
        data_list = pachong(py_name, pagenum)
        print(len(data_list))
        print(data_list)
        if py_name == 'bj':
            for item in data_list:
                models.bjHouseInfo.objects.create(builder=item['builder'], houseType=item['houseType'], \
                                                  area=item['area'], direction=item['direction'], \
                                                  decoration=item['decoration'], floor=item['floor'], \
                                                  year=item['year'], structure=item['structure'], \
                                                  total_price=item['total_price'], unit_price=item['unit_price'])
        return redirect('/showdata/')
    

def showdata(request):
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page-1)*page_size
    end = page*page_size
    py_name = get_first_letter(name)
    if py_name == 'bj':
        data_list = models.bjHouseInfo.objects.all()[start:end]
        total_data = models.bjHouseInfo.objects.all().count()
    page_str_list = []
    prev = '<li><a href="/showdata/?page={}">首页</a></li>'.format(1)
    page_str_list.append(prev)
    total_pagenum, div = divmod(total_data, page_size)
    if div:
        total_pagenum
    plus = 5
    if total_pagenum <= 2*plus+1:
        start_page = 1
        end_page = total_pagenum
    else:
        if page <= plus:
            start_page = 1
            end_page = 2*plus+1
        else:
            if (page + plus)>total_pagenum:
                end_page = total_pagenum
                start_page = total_pagenum - 2*plus
            else:
                start_page = page - plus
                end_page = page + plus
    if page > 1:
        prev = '<li><a href="/showdata/?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="/showdata/?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page+1):
        if i == page:
            ele = '<li class="active"><a href="/showdata/?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="/showdata/?page={}">{}</a></li>'.format(i, i)
        page_str_list.append((ele))
    if page < total_pagenum:
        prev = '<li><a href="/showdata/?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="/showdata/?page={}">下一页</a></li>'.format(total_pagenum)
    page_str_list.append(prev)
    prev = '<li><a href="/showdata/?page={}">尾页</a></li>'.format(total_pagenum)
    page_str_list.append(prev)
    search_string = """
    <form method="get" style="width: 200px">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="页码" name="page">
            <span class="input-group-btn">
                <button class="btn btn-default" type="submit">Go!</button>
            </span>
        </div>
    </form>
    """
    page_str_list.append(search_string)
    page_string = mark_safe(''.join(page_str_list))
    return render(request, 'showdata.html', {"data": data_list, "page_string": page_string})


def sigin(request):
    if request.method == 'GET':
        return render(request, "sigin.html")
    # 获取提交的数据
    name = request.POST.get("username")
    password = request.POST.get("password")
    print(name, password)
    models.UserInfo.objects.create(username=name, password=password)
    return redirect("/mainscene/")


def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    # 获取提交的数据
    name = request.POST.get("username")
    password = request.POST.get("password")
    print(name, password)
    return redirect("/mainscene/")