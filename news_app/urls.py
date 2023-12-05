from django.urls import path
from .views import news_list,news_detail,ContactPageView,blogpage,HomePageView,LocalNewsView,ForeignNewsView,TexnalogNewsView,SportNewsView


urlpatterns = [
    path('',HomePageView.as_view(), name='main'),
    path('all/', news_list, name='news_list'),
    path('<slug:news>',news_detail, name='news_detail'),
    path('contact-us/',ContactPageView.as_view(), name='contact'),
    path('local/',LocalNewsView.as_view(), name='local_page'),
    path('xorij/',ForeignNewsView.as_view(), name='xorij_page'),
    path('texno/',TexnalogNewsView.as_view(), name='texnologiya_page'),
    path('sport/',SportNewsView.as_view(), name='sport_page'),
    path('blog/', blogpage, name='blog')
   
]
