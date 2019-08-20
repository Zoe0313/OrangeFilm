"""
*methods 可接受 任意参数
**kwargs 可接受 多个key=value形式的参数

三层装饰器函数，最外层是用来传参的，看懂内两层就行
"""

import jwt
from django.http import JsonResponse
from user.models import UserProfile

KEY = 'abcdef1234'

def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            # token放在request header -> authorization
            # token = request.META.get('HTTP_AUTHORIZATION')
            token = request.META.get('HTTP_AUTHORIZATION')

            #methods是否有值
            if methods is None:
                #如果没传methods参数，则直接返回视图
                return func(request, *args, **kwargs)

            # 判断当前method是否在*methods参数中，如果在，则进行token校验
            if request.method not in methods:
                #如果当前请求的方法不在methods内，则直接返回视图
                return func(request, *args, **kwargs)
            #严格判断参数大小写，统一大写
            #严格检查methods里的参数是POST、GET、PUT、DELETE

            # 校验token, pyjwt注意 异常检测 'null'
            if token is None or token == 'null':
                result = {'code':107, 'error':'Please give me token'}
                return JsonResponse(result)

            try:
                res = jwt.decode(token,KEY,algorithms='HS256')
            except Exception as e:
                print('--token error is %s'%(e))
                result = {'code':108, 'error':'Please login'}
                return JsonResponse(result)

            # token校验成功，根据用户名取出用户
            username = res['username']
            user = UserProfile.objects.get(username=username)
            if user is None:
                result = {'code':208, 'error':'The user is not existed'}
                return JsonResponse(result)

            request.user = user

            kwargs_name = kwargs.get('username')
            if request.user.username and kwargs_name and request.user.username != kwargs_name:
                raise LoginError("Your username is wrong")
            return func(request, *args, **kwargs)

        return wrapper

    return _login_check

def get_user_by_request(request):
    """
    通过request获取用户
    :param request:
    :return:
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    #检查token
    if token is None or token == 'null':
        return None

    try:
        res = jwt.decode(token, KEY, algorithms='HS256')
    except Exception as e:
        print('--get_user_by_request error is %s' % (e))
        return None

    #获取token中的用户名
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user

class LoginError(Exception):
    """
    自定义异常
    """
    def __init__(self, error_msg):
        self.error = error_msg

    def __str__(self):
        return '<LoginError error %s>'%(self.error)