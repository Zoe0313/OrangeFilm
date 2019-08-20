import datetime
import json

from django.http import JsonResponse

# Create your views here.
from tools.login_decorator import login_check, get_user_by_request
from films.models import Film
from user.models import UserProfile



def films(request, stype, spage):
    if request.method != 'GET':
        result = {'code': 404, 'error': 'not get'}
        return JsonResponse(result)

    ntype = int(stype)
    npage = int(spage)

    film_type = 'now'
    if 2==ntype:
        film_type = 'later'
    elif 3==ntype:
        film_type = 'classic'

    films = Film.objects.filter(stype=film_type)
    result = make_topics_res(films,npage)
    return JsonResponse(result)

def make_topics_res(film_list,offset):
    res = {'code':200, 'data':{}}
    films_res = []

    for film in film_list:
        d = {}
        d['name'] = film.name
        d['type'] = film.stype
        d['duration'] = film.duration
        d['score'] = film.score
        d['stars'] = film.stars[:40]
        d['img_url'] = film.name + film.img_url[-4:]
        d['detail_url'] = film.detail_url
        d['release_time'] = film.release_time
        d['introduce'] = film.content[:220]
        if len(film.content)>220:
            d['introduce'] += '......'
        films_res.append(d)

    count = len(films_res)#总数
    start = offset*10
    end = start+10
    films_res = films_res[start:end]
    res['data']['films'] = films_res
    res['data']['total'] = count
    return res

# @login_check('POST','DELETE')
# def films(request, author_id=None):
#     # /v1/topics/<author_id>
#     if request.method == 'POST':
#         #发表博客 注：发表博客必须为登录状态
#         #当前token中认证通过的用户 即为作者
#         author = request.user
#
#         json_str = request.body
#         if not json_str:
#             result = {'code': 302, 'error': 'Please give me json'}
#             return JsonResponse(result)
#
#         #把json串反序列化成python对象
#         json_obj = json.loads(json_str)
#         title = json_obj.get('title', '')
#         #带全部样式的内容 - content
#         content = json_obj.get('content','')
#         #纯文本的文章内容，用来截取introduce摘要 - content_text
#         content_text = json_obj.get('content_text','')
#         #根据content_text的内容生成文章简介
#         introduce = content_text[:30]
#         limit = json_obj.get('limit')
#         if limit not in ('public','private'):
#             #判断权限是否合法
#             result = {'code':303, 'error':'Please get me right limit'}
#             return JsonResponse(result)
#
#         category = json_obj.get('category')
#         if category not in ('tec','no-tec'):
#             result = {'code':304, 'error':'Please get me right category'}
#             return JsonResponse(result)
#
#         #设置创建时间/修改时间
#         now = datetime.datetime.now()
#
#         try:
#             Film.objects.create(title=title,
#                                  content=content,
#                                  introduce=introduce,
#                                  limit=limit,
#                                  category=category,
#                                  author=author,
#                                  created_time=now,
#                                  modified_time=now)
#         except Exception as e:
#             print('Topic create error is %s' % (e))
#             result = {'code': 305, 'error': 'The topic is existed'}
#             return JsonResponse(result)
#
#         result = {'code':200, 'username':author.username}
#         return JsonResponse(result)
#
#     elif request.method == 'GET':
#         now_films = Film.objects.filter(stype='now')
#
#         result = make_topics_res(now_films)
#         return JsonResponse(result)
#         #/v1/topics/liuxiaoxia
#         #获取用户博客列表/具体博客内容【带?t_id=xx】
#         #1. 访问当前博客的 访问者 - visitor
#         #2. 当前博客的博主 - author
#
#         # authors = UserProfile.objects.filter(username=author_id)
#         # if authors is None:
#         #     result = {'code':306, 'error':'The current author is not existed'}
#         #     return JsonResponse(result)
#         #
#         # #当前访问的博客的博主
#         # author = authors[0]
#         #
#         # visitor = get_user_by_request(request)
#         # visitor_name = None
#         # if visitor:
#         #     visitor_name = visitor.username
#         #
#         # #尝试获取t_id，如果有t_id则证明当前请求是获取用户指定
#         # #/v1/topics/guoxiaonao?t_id=1
#         # t_id = request.GET.get('t_id')
#         # if t_id:
#         #     #取指定t_id的博客
#         #     t_id = int(t_id)
#         #     try:
#         #         author_topic = Film.objects.get(id=t_id)
#         #         if visitor_name != author_id:
#         #             author_topic = Film.objects.get(id=t_id, limit='public')
#         #     except Exception as e:
#         #         return JsonResponse({'code': 309, 'error': 'This topic is not existed'})
#         #
#         #     res = make_topic_res(author,author_topic,visitor_name,author_id)
#         #     return res
#         #
#         # category = request.GET.get('category')
#         # # 判断category取值范围
#         # if category in ('tec','no-tec'):
#         #     if visitor_name == author_id:
#         #         author_topics = Film.objects.filter(author_id=author_id, category=category)
#         #     else:
#         #         author_topics = Film.objects.filter(author_id=author_id, limit='public', category=category)
#         # else:
#         #     #对比两者的username是否一致，从而判断当前是否要取private的博客
#         #     if visitor_name == author_id:
#         #         #博主在访问自己的博客，此时获取用户全部权限的博客
#         #         author_topics = Film.objects.filter(author_id=author_id)
#         #     else:
#         #         #其他访问者在访问当前博客
#         #         author_topics = Film.objects.filter(author_id=author_id, limit='public')
#         #
#         # result = make_topics_res(author, author_topics)
#         # return JsonResponse(result)
#
#     elif request.method == 'DELETE':
#         #删除博主的博客文章
#         author = request.user
#         if author_id != author.username:
#             result = {'code':306,'error':'You can not delete it'}
#             return JsonResponse(result)
#         #当token中用户名和url中的author_id严格一致的时候，方可执行删除
#
#         delete_id = request.GET.get('topic_id')
#         if not delete_id:
#             result = {'code':307,'error':'You can not do it !!'}
#             return JsonResponse(result)
#
#         try:
#             #查询准备删除的topic
#             topic = Film.objects.get(id=delete_id)
#         except Exception as e:
#             #如果当前topic不存在，则返回异常
#             print('Topic delete error is %s' % (e))
#             result = {'code':308, 'error':'Your topic is not existed'}
#             return JsonResponse(result)
#
#         topic.delete()
#         return JsonResponse({'code':200})
#     return JsonResponse({'code':200,'username':1})
#
# def make_topic_res(author,author_topic, visitor_name, author_id):
#     """
#     生成具体博客内容的返回值
#     :param author
#     :param author_topic:
#     :param visitor_name:
#     :param author_id
#     :return:
#     """
#
#     topic_id = author_topic.id
#
#     next_topic_id = None
#     next_topic_title = None
#     try:
#         #访问博主自己的文章
#         next_topic = Film.objects.filter(id__gt=topic_id,author=author).first()
#         if visitor_name != author_id:#当前访问者不是博主
#             next_topic = Film.objects.filter(id__gt=topic_id, limit='public').first()
#         next_topic_id = next_topic.id
#         next_topic_title = next_topic.title
#     except Exception as e:
#         print('No next topic')
#
#     prev_topic_id = None
#     prev_topic_title = None
#     try:
#         prev_topic = Film.objects.filter(id__lt=topic_id,author=author).last()
#         if visitor_name!=author_id:
#             prev_topic = Film.objects.filter(id__lt=topic_id, limit='public').last()
#         prev_topic_id = prev_topic.id
#         prev_topic_title = prev_topic.title
#     except Exception as e:
#         print('No prev topic')
#
#     data = {}
#     data["nickname"] = author_topic.author.nickname
#     data["title"] = author_topic.title
#     data["category"] = author_topic.category
#     data["created_time"] = author_topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
#     data["content"] = author_topic.content
#     data["introduce"] = author_topic.introduce
#     data["author"] = author_topic.author.nickname
#     data["next_id"] = next_topic_id
#     data["next_title"] = next_topic_title
#     data["last_id"] = prev_topic_id
#     data["last_title"] = prev_topic_title
#
#     return JsonResponse({'code': 200, 'data': data})
"""
    #生成message返回结构
    #拿出所有该topic的message，并按时间倒序排序
    all_messages = Message.objects.filter(topic=author_topic).order_by('-created_time')
    msg_list = []
    level1_msg = {}#key是留言ID，value是[回复对象,回复对象,...]
    for msg in all_messages:
        parent_id = msg.parent_message
        if parent_id:
            #回复
            level1_msg.setdefault(msg.parent_message,[])#初始化
            level1_msg[parent_id].append({
                'msg_id': msg.id,
                'content': msg.content,
                'publisher': msg.publisher.nickname,
                'publisher_avatar': str(msg.publisher.avatar),
                'created_time': msg.created_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            #一级留言
            msg_list.append({
                'id':msg.id,
                'content':msg.content,
                'publisher':msg.publisher.nickname,
                'publisher_avatar':str(msg.publisher.avatar),
                'created_time':msg.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                'reply':[]
            })


    for msg in msg_list:
        if msg['id'] in level1_msg:
           msg['reply'] = level1_msg[msg['id']]

    data["messages"] = msg_list
    data["messages_count"] = all_messages.count()
"""

