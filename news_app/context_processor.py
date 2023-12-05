from .models import News,Category



def latest_news(request):
  latest_news = News.published.all().order_by("-publish_time")[:5]
  cotegories = Category.objects.all()

  context = {
    'latest_news':latest_news,
    'cotegories':cotegories
  }

  return context