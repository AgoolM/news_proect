from django.urls import path
from .views import news_list,news_detail,ContactPageView,blogpage,HomePageView,LocalNewsView,ForeignNewsView,TexnalogNewsView,SportNewsView,NewsDeleteView,NewsUpdateView,NewsCresteView,admin_page_view,SearchResultsList


urlpatterns = [
    path('',HomePageView.as_view(), name='main'),
    path('all/', news_list, name='news_list'),
    path('news/create/',NewsCresteView.as_view(),name='news_create'),
    path('news/<slug:news>',news_detail, name='news_detail'),
    path('news/<slug>/edit/',NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/',NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/',ContactPageView.as_view(), name='contact'),
    path('local/',LocalNewsView.as_view(), name='local_page'),
    path('xorij/',ForeignNewsView.as_view(), name='xorij_page'),
    path('texno/',TexnalogNewsView.as_view(), name='texnologiya_page'),
    path('sport/',SportNewsView.as_view(), name='sport_page'),
    path('blog/', blogpage, name='blog'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('search/',SearchResultsList.as_view(), name='searchpage'),
    #path('news/<slug:news>/', NewsDetailView.as_view(), name='news_detail'),
   
]
