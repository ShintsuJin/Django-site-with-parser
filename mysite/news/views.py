from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News
from .serializers import ArticleSerializer


class NewsAPI(APIView):
    def get(self, request):
        articles = News.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post_new": serializer.data})


class HomeNews(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'HomePage'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)



#def news(request):
    #news = News.objects.select_related('category').all()
    #context = {
    #    'news': news,
    #    'title': 'A list of breaking news',
    #}
    #return render(request, 'news/news.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id).select_related('category')
    category = Category.objects.get(id=category_id)
    return render(request, 'news/category.html', {'news': news,  'category': category})


def view_news(request, id):
    news_item = get_object_or_404(News, pk=id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            #news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm
    return render(request, 'news/add_news.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect('login')
        else:
            messages.error(request, 'Oops, something is wrong :(')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')



#def pagination(request):
#    news_list = News.objects.all()
#   paginator = Paginator(news_list, 3)
#    page_num = request.GET.get('page')
#    page_obj = paginator.get_page(page_num)
#   return render(request, 'news/pagination.html', {'page_obj': page_obj})