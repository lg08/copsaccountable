from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path(                       # list of all posts ever
        '',
        views.PostList.as_view(),
        name="all"
    ),
    path(                       # create a new post
        "new/",
        views.form_create_view,
        name="create"
    ),
    path(                       # shows the post in detail
        "by/<int:pk>/",
        views.PostDetail.as_view(),
        name="detail"
    ),
    path(                       # deletes a post
        "delete/<int:pk>/",
        views.DeletePost.as_view(),
        name='delete'
    ),
    path(
        'profile/of/<username>/',
        views.UserPage.as_view(),
        name='user_page'
    ),  # user profile page
    path(
        'search/',
        views.SearchResultsView.as_view(),
        name='search'
    ),  # search results page
    path(
        'worst_posts/',
        views.WorstPostsView.as_view(),
        name='worst_posts'
    ),  # top 30 worst posts
    path(
        'best_posts/',
        views.BestPostsView.as_view(),
        name='best_posts'
    ),  # top 30 best posts

    # function-based views
    path(
        'upvote/<int:pk>',
        views.UpvoteView,
        name='upvote_post'
    ),
    path(
        'downvote/<int:pk>',
        views.DownvoteView,
        name='downvote_post'
    ),
    path(
        'create/comment/<int:subcomment>/on/<int:postpk>/<int:commentpk>/',
        views.create_comment,
        name='create_comment'
    ),

]
