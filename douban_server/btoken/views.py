from django.http import JsonResponse
import hashlib
import time
import jwt
import json

from user.models import UserProfile

def make_token(email,expire=3600*24):
    '''
    生成token
    :param username:
    :param expire:
    :return:
    '''

    key = 'abcdef1234'
    now_t = time.time()
    payload = {'email':email, 'exp':int(now_t)+expire}
    return jwt.encode(payload, key, algorithm='HS256')


# Create your views here.
def btoken(request):
    if not request.method == 'POST':
        result = {'code':101, 'error':'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    print(json_str)

    if not json_str:
        result = {'code':102, 'error':'Please POST data'}
        return JsonResponse(result)

    json_obj = json.loads(json_str)
    #获取邮箱名和密码
    email = json_obj.get('email')
    password = json_obj.get('password')

    if not email:
        result = {'code':103, 'error':'Please give me email'}
        return JsonResponse(result)

    if not password:
        result = {'code':104, 'error':'Please give me password'}
        return JsonResponse(result)

    #检查用户是否存在
    users = UserProfile.objects.filter(email=email)
    if not users:
        #该用户未注册
        result = {'code':105, 'error':'The user is not existed'}
        return JsonResponse(result)

    #hash password
    s1 = hashlib.sha1()
    s1.update(password.encode())
    if s1.hexdigest() != users[0].password:
        result = {'code':106, 'error':'The username is wrong or the password is wrong'}
        return JsonResponse(result)

    #make token
    token = make_token(email)
    result = {'code':200,
              'email':email,
              'nickname':users[0].nickname,
              'data':{'token':token.decode()}}
    return JsonResponse(result)