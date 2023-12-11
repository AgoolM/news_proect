from django.contrib import admin
from . models import News ,Category,Contact,Comsent

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display=['title','slug','category','publish_time','status']
  list_filter=['status','created_time','publish_time','category']
  prepopulated_fields={"slug":('title',)}
  date_hierarchy='publish_time'
  search_fields=['title','bodiy']
  ordering=['status','publish_time',]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display=['id','name']

admin.site.register(Contact)

class CommentAdmin(admin.ModelAdmin):
  list_display = ['user','body','created_time','active']
  list_filter = ['active','created_time']
  search_fields = ['user','body']

  def disable_comments(self, request, queryset):
    queryset.update(active=False)
  
  def active_comments(self,request,queryset):
    queryset.update(active=True)

admin.site.register(Comsent,CommentAdmin)