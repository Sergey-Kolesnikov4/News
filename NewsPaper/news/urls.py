from django.urls import path
from .views import (NewsList,NewsDetail,SearchList,NewsCreate,ArticleCreate,
NewsUpdate,ArticleUpdate,NewsDelete,ArticleDelete,CategoryList,subscribe)

urlpatterns = [
    path('', NewsList.as_view(), name = 'news_list'),
    path('<int:pk>',NewsDetail.as_view(),name = 'news_detail'),
    path('search/',SearchList.as_view(), name = 'search_list'),
    path('NW/create/',NewsCreate.as_view(), name = 'news_create'),
    path('AR/create/',ArticleCreate.as_view(), name = 'article_create'),
    path('NW/<int:pk>/update/',NewsUpdate.as_view(), name = 'news_update'),
    path('AR/<int:pk>/update/',ArticleUpdate.as_view(), name = 'article_update'),
    path('NW/<int:pk>/delete/',NewsDelete.as_view(), name = 'news_delete'),
    path('AR/<int:pk>/delete/',ArticleDelete.as_view(), name = 'article_delete'),
    path('categories/<int:pk>',CategoryList.as_view(), name = 'category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
     ]