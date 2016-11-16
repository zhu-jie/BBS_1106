from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
# Create your models here.
#调用ValidationError方法显示红色报错
class Article(models.Model):
    '''用于存放文章
    包含字段：
    文章titil,可重名，最大长度255，且不能为空
    文章简介brief
    文章分类category,应该和下面的category类关联
    '''
    title = models.CharField(max_length=255,verbose_name="标题")
    brief = models.CharField(null=True,blank=True,max_length=255,verbose_name="描述")
    category = models.ForeignKey("Category",verbose_name="标签")
    content = models.TextField(u"文章内容")
    author = models.ForeignKey("UserProfile",verbose_name="作者")
    pub_data = models.DateTimeField(blank=True,null=True,verbose_name="修改时间") #发布时间
    last_modify = models.DateTimeField(auto_now=True,verbose_name="最后操作事件")
    priority = models.IntegerField(u"优先级",default=1000)
    head_img = models.ImageField(u"文章标题图片",upload_to="uploads")  #指定上传路径
    status_choices = (('draft',u'草稿'),
                      ('published',u'已发布'),
                      ('hidden',u'隐藏'),)
    status = models.CharField(choices=status_choices,default='published',max_length=32,verbose_name="状态")
    class Meta:
        verbose_name_plural = "文章"
    def __str__(self):
        return self.title
    def clean(self):
        if self.status ==  'draft' and self.pub_data is not None:
            raise ValidationError(('Drafy entries may not have a publication date.'))
        if self.status == 'published' and self.pub_data is None:
            self.pub_data = datetime.date.today()
class Comment(models.Model):
    '''评论，和点赞'''
    article = models.ForeignKey(Article,verbose_name=u"所属文章")
    parent_comment = models.ForeignKey('self',related_name='my_children',blank=True,null=True)
    comment_choice = ((1,u'评论'),
                      (2,u'点赞'))
    comment_type = models.IntegerField(choices=comment_choice,default=1)
    user = models.ForeignKey("UserProfile")
    comment = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "评论"
    def clean(self):
        if self.comment_type == 1 and len(self.comment) == 0:
            raise ValidationError('评论不能为空，sb')
    def __str__(self):
         return "%s.P:%s,%s" %(self.article,self.parent_comment.id,self.comment)

class Category(models.Model):
    '''板块'''
    name = models.CharField(max_length=64)
    brief = models.CharField(null=True,blank=True,max_length=255)
    set_as_top_menu = models.BooleanField(default=False)
    postion_index = models.SmallIntegerField()
    admins = models.ManyToManyField("UserProfile",blank=True)
    class Meta:
        verbose_name_plural = "标签"
    def __str__(self):
        return self.name
class UserProfile(models.Model):
    '''用户,引用django自带的'''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    signature = models.CharField(max_length=255,blank=True,null=True)
    head_img = models.ImageField(height_field=150,width_field=150,blank=True,null=True) #头像大小
    class Meta:
        verbose_name_plural = "用户"
    def __str__(self):
        return self.name
