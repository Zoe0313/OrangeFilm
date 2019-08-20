from django.db import models

# Create your models here.

class Film(models.Model):
    #主键为id,django默认添加

    name = models.CharField('电影名称', max_length=50, default='')
    stype = models.CharField('上映情况', max_length=10, default='now')
    duration = models.CharField('电影时长', max_length=20, default='100分钟')
    region = models.CharField('上映地区', max_length=20, default='')
    score = models.FloatField('评分', default=0.0)
    stars = models.CharField('演员表', max_length=300, default='')
    img_url = models.CharField('海报链接', max_length=200, default='')
    detail_url = models.CharField('详情界面链接', max_length=200, default='')
    release_time = models.CharField('上映时间', max_length=100, default='')
    introduce = models.CharField('概要',max_length=90, default='')
    content = models.TextField('内容', default='')

    class Meta:
        db_table = 'film'