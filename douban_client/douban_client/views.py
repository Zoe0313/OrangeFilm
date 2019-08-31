from django.shortcuts import render

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def index(request):
    return render(request,'index.html')

def films(request,ntype,npage=None):
    #print(npage)
    if not npage:
        npage=0

    filmtype = '热门电影'
    if '2'==ntype:
        filmtype = '即将上映'
    elif '3'==ntype:
        filmtype = '经典电影'
    return render(request, 'list.html',locals())

def search(request):
    key = request.GET.get('key')
    print(key)
    filmtype = '搜索结果'
    return render(request, 'search.html', locals())

def notexist(request):
    return render(request, '404.html')