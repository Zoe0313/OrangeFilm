from django.http import JsonResponse
import hashlib
import json

from tools.login_decorator import login_check
from user.models import UserProfile
from btoken.views import make_token

@login_check('PUT','DELETE')
def users(request, username=None):
    if request.method == 'GET':
        # 取数据
        # /v1/users/liuxiaoxia?info=1 {'info':xxx}
        if username:
            # 具体用户的数据
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                user = None

            if not user:
                result = {'code': 208, 'error': 'The user is not existed'}
                return JsonResponse(result)

            # 判断查询字符串
            if request.GET.keys():
                # 证明有查询字符串
                data = {}
                for k in request.GET.keys():
                    # 数据库中最好是有非空默认值
                    if hasattr(user, k):
                        data[k] = getattr(user, k)
                result = {'code': 200, 'username': username, 'data': data}
                return JsonResponse(result)
            else:
                # 证明指定查询用户全量数据
                result = {'code': 200, 'username': username, 'data': {
                    'info': user.info,
                    'sign': user.sign,
                    'nickname': user.nickname,
                    'avatar': str(user.avatar)
                }}
                return JsonResponse(result)
        else:
            # 全部用户的数据
            # UserProfile获取全部用户的数据
            all_users = UserProfile.objects.all()
            res = []
            for u in all_users:
                d = {}
                d['username'] = u.username
                d['email'] = u.email
                res.append(d)
                print(d)

            result = {'code': 200, 'data': res}
            return JsonResponse(result)
    elif request.method == 'POST':
        #注册用户
        #密码需要SHA-1 hashlib.sha1() -> update -> hexdigest()

        #获取json数据
        json_str = request.body
        print(json_str)

        if not json_str:
            result = {'code':202, 'error':'Please POST data'}
            return JsonResponse(result)

        #反序列话json_str
        json_obj = json.loads(json_str)
        nickname = json_obj.get('nickname','')
        email = json_obj.get('email','')
        password = json_obj.get('password')

        if not nickname:
            result = {'code':203, 'error':'Please give me nickname'}
            return JsonResponse(result)

        if not email:
            result = {'code':204, 'error':'Please give me email'}
            return JsonResponse(result)

        if not password:
            result = {'code':205, 'error':'Please give me password'}
            return JsonResponse(result)

        #检查用户是否存在
        old_email = UserProfile.objects.filter(email=email)
        if old_email:
            #该用户已经注册
            result = {'code':207, 'error':'The email is existed'}
            return JsonResponse(result)

        s1 = hashlib.sha1()
        s1.update(password.encode())
        try:
            UserProfile.objects.create(nickname=nickname,email=email,password=s1.hexdigest())
        except Exception as e:
            print('UserProfile create error is %s'%(e))
            result = {'code': 207, 'error': 'The email is existed'}
            return JsonResponse(result)

        #make token
        token = make_token(email)
        result = {'code':200,
                  'nickname':nickname,
                  'email':email,
                  'data':{'token':token.decode()}}
        return JsonResponse(result)

    elif request.method == 'PUT':
        #修改用户数据
        #前端返回的json格式{'nickname':xxx, 'sign':xxx, 'info':xxx}
        json_str = request.body
        #print(json_str)

        #判断前端是否给了json
        if not json_str:
            result = {'code':202, 'error':'Please give me data'}
            return JsonResponse(result)

        if not username:
            result = {'code':203, 'error':'Please give me username'}
            return JsonResponse(result)

        #检查用户是否存在
        user = request.user

        json_obj = json.loads(json_str)
        nickname = json_obj.get('nickname', '')
        sign = json_obj.get('sign','')
        info = json_obj.get('info','')

        if not nickname:
            #昵称不能为空
            result = {'code':209, 'error':'nickname is none!'}
            return JsonResponse(result)

        #存
        user.nickname = nickname
        user.sign = sign
        user.info = info
        user.save()

        result = {'code':200, 'username':username}
        return JsonResponse(result)
    return JsonResponse({'code':200, 'username':1})

@login_check('POST')
def user_avatar(request, username=None):
    # 上传图片思路：
    # 1. 前端-> form提交 并且 content-type要改成 multipart/form-data
    # 2. 后端只要拿到post提交，request.FILES['avatar']
    # 注意：由于目前django获取put请求的multipart数据较为复杂，故改为post获取multipart数据

    #当前必须是POST提交
    if not request.method == 'POST':
        result = {'code':210, 'error':'Please use POST'}
        return JsonResponse(result)

    if not username:
        result = {'code':203, 'error':'Please give me username'}
        return JsonResponse(result)

    user = request.user

    avatar = request.FILES.get('avatar')
    if avatar:
        #正常提交图片信息，进行存储
        print('avatar:',avatar)
        user.avatar = avatar
        user.save()
        result = {'code':200, 'username':username}
        return JsonResponse(result)
    else:
        #没有提交图片信息
        result = {'code':211, 'error':'Please give me avatar'}
        return JsonResponse(result)

