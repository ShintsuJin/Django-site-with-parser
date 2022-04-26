from django.urls import path
from . import views
from .views import HomeNews
from django.views.decorators.cache import cache_page
from .views import NewsAPI


urlpatterns = [
    path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('api/news/', NewsAPI.as_view(), name='news'),
    path('category/<int:category_id>/', views.get_category, name='category'),
    path('news/<int:id>/', views.view_news, name='view_news'),
    path('news/add_news', views.add_news, name='add_news'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]