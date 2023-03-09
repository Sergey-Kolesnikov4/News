from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .filters import NewsFilter
from .forms import NewsForm,ArticleForm
from .models import News,Category




class NewsList(ListView):
    model = News
    ordering = '-dateCreation'
    template_name = 'index.html'
    context_object_name = 'news'
    paginate_by = 5




class SearchList(ListView):
    model = News
    ordering = '-dateCreation'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 5



    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class NewsDetail(DetailView):
    model = News
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'create_news.html'
    raise_exception = True

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = 'NW'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('post.add_post',)
    form_class = ArticleForm
    model = News
    template_name = 'create_article.html'
    raise_exception = True

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'create_news.html'
    raise_exception = True


class ArticleUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('post.change_post',)
    form_class = ArticleForm
    model = News
    template_name = 'create_article.html'
    raise_exception = True


class NewsDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class ArticleDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('post.delete_post',)
    model = News
    template_name = 'delete_articles.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

class CategoryList(ListView):
    model = News
    paginate_by = 5
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category,id = self.kwargs['pk'])
        queryset = News.objects.filter(category = self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_signed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(requests, pk):
    user=requests.user
    category=Category.objects.get(id=pk)
    category.subscribers.add(user)
    message='Вы успешно подписались на рассылку новостей категории'
    return render (requests,'subscribe.html',{'category': category,'message':message})


