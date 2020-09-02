from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('', views.PostList.as_view(), name="all"),

    path("new/", views.my_custom_form_view, name="create"),
    
    path("by/<username>/", views.UserPosts.as_view(),name="for_user"),
    path("by/<username>/<int:pk>/", views.PostDetail.as_view(),name="detail"),
    path("delete/<int:pk>/", views.DeletePost.as_view(),name="delete"),

    path('upvote/<int:pk>', views.UpvoteView, name='upvote_post'),
    path('downvote/<int:pk>', views.DownvoteView, name='downvote_post'),
    path('profile/of/<username>/', views.UserPage.as_view(), name='user_page'),

    path('create/comment/<int:subcomment>/on/<int:postpk>/<int:commentpk>/', views.create_comment, name='create_comment'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('worst_posts/', views.WorstPostsView.as_view(), name='worst_posts'),
    path('best_posts/', views.BestPostsView.as_view(), name='best_posts'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here

]
