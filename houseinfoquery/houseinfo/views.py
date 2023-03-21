from django.shortcuts import render, redirect
from pypinyin import lazy_pinyin, Style
import requests
import parsel

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
        return redirect('/showdata/')
