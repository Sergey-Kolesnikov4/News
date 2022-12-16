from django.urls import path
from .views import NewsList,NewsDetail,SearchList,NewsCreate,ArticleCreate,NewsUpdate,ArticleUpdate,NewsDelete,ArticleDelete

urlpatterns = [
    path('', NewsList.as_view(), name = 'news_list'),
    path('<int:id>',NewsDetail.as_view(),name = 'news_detail'),
    path('search/',SearchList.as_view(), name = 'search_list'),
    path('NW/create/',NewsCreate.as_view(), name = 'news_create'),
    path('AR/create/',ArticleCreate.as_view(), name = 'article_create'),
    path('NW/<int:id>/update/',NewsUpdate.as_view(), name = 'news_update'),
    path('AR/<int:id>/update/',ArticleUpdate.as_view(), name = 'article_update'),
    path('NW/<int:id>/delete/',NewsDelete.as_view(), name = 'news_delete'),

    path('AR/<int:id>/delete/',ArticleDelete.as_view(), name = 'article_delete'),

    ]