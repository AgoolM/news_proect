from typing import Any
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView
from django.http import HttpResponse
from .models import News, Category
from .forms import ContactForm


def news_list(request):
  news_list=News.objects.filter(status=News.Status.Published)
  #news_list=News.published.all()
  context={
    'news_list':news_list
  }
  return render(request,'news/news_list.html',context=context)


def news_detail(request,news):
  news = get_object_or_404(News,slug=news, status=News.Status.Published)
  context={
    "news":news
  }
  return render(request,'news/news_detail.html',context)

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
       context['mahalliy_news'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[0:6]
       context['xorij_news'] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[0:6]
       context['sport_news'] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[0:6]
       context['texno_news']=News.published.all().filter(category__name="Texnalogiya").order_by("-publish_time")[0:6]

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
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news
   


class ForeignNewsView(ListView):
   model = News
   template_name = 'news/xorij.html'
   context_object_name = 'xorji_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name='Xorij')
      return news


class TexnalogNewsView(ListView):
   model = News
   template_name = 'news/texnalogiya.html'
   context_object_name = 'texnalogik_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name='Texnalogiya')
      return news

class SportNewsView(ListView):
   model = News
   template_name = 'news/sport.html'
   context_object_name = 'sport_yangiliklar'

   def get_queryset(self):
      news = self.model.published.all().filter(category__name='Sport')
      return news

