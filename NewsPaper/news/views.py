from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from .filters import NewsFilter
from .forms import NewsForm,ArticleForm
from .models import News



class NewsList(ListView):
    model = News
    ordering = 'title'
    template_name = 'index.html'
    context_object_name = 'news'
    paginate_by = 5



class SearchList(ListView):
    model = News
    ordering = 'title'
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
    pk_url_kwarg = 'id'


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
    pk_url_kwarg = 'id'


class ArticleUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('post.change_post',)
    form_class = ArticleForm
    model = News
    template_name = 'create_article.html'
    pk_url_kwarg = 'id'


class NewsDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')
    pk_url_kwarg = 'id'


class ArticleDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('post.delete_post',)
    model = News
    template_name = 'delete_articles.html'
    success_url = reverse_lazy('news_list')
    pk_url_kwarg = 'id'

