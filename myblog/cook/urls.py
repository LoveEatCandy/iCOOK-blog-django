from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='cook'
urlpatterns = [
    path('',views.index,name='index'),
    path('recipes/<slug:foodstyle>/',views.recipes,name='recipes'),
    path('search/',views.search,name='search'),
    path('<int:article_id>/',views.single,name='single'),
    path('about/',views.about,name='about'),
    path('user/',views.person,name='person'),

    #收藏
    path('add_fav/',views.FavorateView.as_view(),name='add_fav'),
    #评论
    path('comment/',views.AddCommentView.as_view(),name='comment'),
    #回复1
    path('reply1/',views.AddReply1View.as_view(),name='reply1'),
    #回复2
    path('reply2/',views.AddReply2View.as_view(),name='reply2'),
    #删除评论
    path('comment_delete/',views.DeleteCommentView.as_view(),name='comment_delete'),
    #删除回复
    path('reply_delete/',views.DeleteReplyView.as_view(),name='reply_delete'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)