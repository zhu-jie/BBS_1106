from django.contrib import admin
from bbs import models
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    '''自定义admin展示的内容'''
    list_display = ('title','category','author','pub_data','last_modify','status','priority')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','parent_comment','comment_type','comment','user','date')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','set_as_top_menu','postion_index')
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Category,CategoryAdmin)