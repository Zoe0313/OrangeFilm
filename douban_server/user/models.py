from django.db import models

# Create your models here.
class UserProfile(models.Model):
    email = models.CharField('邮箱',max_length=50,primary_key=True)
    nickname = models.CharField('昵称',max_length=30)
    password = models.CharField('密码',max_length=40)
    sign = models.CharField('签名',max_length=50,default='')
    info = models.CharField('描述',max_length=150,default='')
    avatar = models.ImageField('头像',upload_to='avatar/')

    class Meta:
        db_table = 'user_profile'