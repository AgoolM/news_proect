from audioop import reverse
from typing import Any
from django.views import View
from hitcount.views import HitCountDetailView,HitCountMixin
from hitcount.utils import get_hitcount_model
from django.contrib.auth.models import User
from django.db.models import Q 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render,get_object_or_404
from django.views.generic import TemplateView,ListView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Contact, News, Category ,Comsent
from .forms import ContactForm ,CommentForm
from config.custom_permissions import OnlyLoggedSuperUser
import gettext



def news_list(request):
  news_list=News.objects.filter(status=News.Status.Published)
  #news_list=News.published.all()
  context={
    'news_list':news_list
  }
  return render(request,'news/news_list.html',context=context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        "comments": comments,
        'comment_count':comment_count,
        "new_comment": new_comment,
        "comment_form": comment_form
    }

    return render(request, 'news/news_detail.html', context)


# def news_detail(request,news):
#   news = get_object_or_404(News,slug=news, status=News.Status.Published)
#   context ={}
#   #hitcount logic 
#   hit_count =get_hitcount_model().objects.get_for_object(news)
#   hits=hit_count.hits
#   hitcontext = context['hitcount'] = {'pk':hit_count.pk}
#   hit_count_response = HitCountMixin.hit_count(request, hit_count)
#   if hit_count_response.hit_counted:
#      hits=hits+1
#      hitcontext['hit_counted'] = hit_count_response.hit_counted
#      hitcontext['total_hits']=hits
#   comments = news.comments.filter(active=True)
#   new_comment = None
#   if request.method =="POST":
#      comment_form = CommentForm(data=request.POST)
#      if comment_form.is_valid():
#         #yagi komment obyektini yaratamiz lekin DB saqalamymiz 
#         new_comment = comment_form.save(commit=False)
#         new_comment.news = news
#         #izoh egasini userga bog'ladik 
#         new_comment.user = request.user
#         #ma'lumotlar bazasiga sqalaqymiz 
#         new_comment.save()
#         comment_form = CommentForm()
       
#   else:
#      comment_form = CommentForm()

#   context={
#     "news":news,
#     "comments":comments,
#     "new_comment":new_comment,
#     "comment_form":comment_form
#   }
#   return redirect(reverse("news_detail", kwargs={'pk': news.id}))

# class NewsDetailView(View):
    
#     def get(self, request, news):
#         news = get_object_or_404(News, slug=news, status=News.Status.Published)
#         comments = news.comments.filter(active=True)
#         comment_form = CommentForm()
        
#         context = {
#             "news": news,
#             "comments": comments,
#             "comment_form": comment_form
#         }
#         return render(request, 'news/news_detail.html', context)

#     def post(self, request, news):
#         news = get_object_or_404(News, slug=news, status=News.Status.Published)
#         comments = news.comments.filter(active=True)
#         comment_form = CommentForm(data=request.POST)
#         new_comment = None

#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.news = news
#             new_comment.user = request.user
#             new_comment.save()
#             comment_form = CommentForm()

#         context = {
#             "news": news,
#             "comments": comments,
#             "new_comment": new_comment,
#             "comment_form": comment_form
#         }
#         return render(request, 'news/news_detail.html', context)
# class NewsDetailView(HitCountDetailView, View):
#     model = News
#     count_hit = True
#     template_name = 'news/news_detail.html'
# def homePageView(request):
#   categories = Category.objects.all()
#   news_list = News.published.all().order_by('-publish_time')[:5]
#   local_one = News.published.filter(category__name ="Mahalliy").order_by("-publish_time")[:1]
#   local_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[0:6]
#   global_one = News.published.filter(category__name ="Xorij").order_by("-publish_time")[:1]
#   global_news = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[0:6]
#   sport_one = News.published.filter(category__name ="Sport").order_by("-publish_time")[:1]
#   sport_news = News.published.all().filter(category__name="Sport").order_by("-publish_time")[0:6]
#   texno_one = News.published.filter(category__name ="Texnalogiya").order_by("-publish_time")[:1]
#   texno_news = News.published.all().filter(category__name="Texnalogiya").order_by("-publish_time")[0:6]
#   context = {
#      "categories":categories,
#      "news_list":news_list,
#      "local_one":local_one,
#      "local_news":local_news,
#      "global_one":global_one,
#      "global_news":global_news,
#      "sport_one":sport_one,
#      "sport_news":sport_news,
#      "texno_one":texno_one,
#      "texno_news":texno_news




#   }
  
#   return render(request,'news/home.html',context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['categories'] = Category.objects.all()
       context['news_list'] = News.published.all().order_by('-publish_time')[:5] 
       context['mahalliy_news'] = News.published.all().filter(category__name_uz="Mahalliy").order_by("-publish_time")[0:6]
       context['xorij_news'] = News.published.all().filter(category__name_uz="Xorij").order_by("-publish_time")[0:6]
       context['sport_news'] = News.published.all().filter(category__name_uz="Sport").order_by("-publish_time")[0:6]
       context['texno_news']=News.published.all().filter(category__name_uz="Texnalogiya").order_by("-publish_time")[0:6]

       return context

   

# def contact_page(request):
#   return render(request,'news/contact.html')


# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()

#         return HttpResponse("<h2> Biz bilan aloqa qilganingiz uchun tashakur !")
#     context = {
#        "form":form
#     }
#     return render (request,'news/contact.html',context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
       form = ContactForm()
       context = {
          "form":form
       }
       return render(request, 'news/contact.html', context)
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method =="POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan aloqa qilganingiz uchun tashakur !")
        context = {
          "form":form
       }
        return render(request, 'news/contact.html', context)
        

def blogpage(request):
   return render(request,'news/blog.html')   
    


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahlliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz='Mahalliy')
        return news
   


class ForeignNewsView(ListView):
   model = News
   template_name = 'news/xorij.html'
   context_object_name = 'xorji_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name_uz='Xorij')
      return news


class TexnalogNewsView(ListView):
   model = News
   template_name = 'news/texnalogiya.html'
   context_object_name = 'texnalogik_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name_uz='Texnalogiya')
      return news

class SportNewsView(ListView):
   model = News
   template_name = 'news/sport.html'
   context_object_name = 'sport_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name_uz='Sport')
      return news


class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
   model = News
   fields = ('title','body','image','category','status')
   template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
   model = News
   template_name = 'crud/news_delete.html'
   success_url = reverse_lazy('main')


class NewsCresteView(OnlyLoggedSuperUser,CreateView):
   model = News
   fields = ('title','title_uz','title_en','title_ru','slug','body','body_uz','body_en','body_ru','image','category','status')
   template_name = "crud/news_create.html"
   #success_url = reverse_lazy('main')

@login_required
@user_passes_test(lambda u : u.is_superuser)
def admin_page_view(request):
   admin_users = User.objects.filter(is_superuser=True)
   context = {
      "admin_users": admin_users
   }
   return render(request, 'pagest/admin_page.html', context)


class SearchResultsList(ListView):
   model = News
   template_name = "news/search_result.html"
   context_object_name = 'barcha_yangiliklar'

   def get_queryset(self):
      query = self.request.GET.get('q')

      return News.objects.filter(
         Q(title__icontains=query)| Q(body__icontains=query)
         ) 