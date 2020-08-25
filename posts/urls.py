from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('', views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),
    path("by/<username>/", views.UserPosts.as_view(),name="for_user"),
    path("by/<username>/<int:pk>/", views.PostDetail.as_view(),name="detail"),
    path("delete/<int:pk>/", views.DeletePost.as_view(),name="delete"),

    path('upvote/<int:pk>', views.UpvoteView, name='upvote_post'),
    path('downvote/<int:pk>', views.DownvoteView, name='downvote_post'),
]
