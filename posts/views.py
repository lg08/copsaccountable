from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from . import models
from posts.models import Upvote, Downvote
from django.urls import reverse
# from django.core.files.storage import FileSystemStorage

# pip install django-braces
from braces.views import SelectRelatedMixin

from . import forms
from . import models
from . import views
from . import urls

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "city")  # not entirely sure what this does yet
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "city")

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(
    #         user__username__iexact=self.kwargs.get("username")
    #     )

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # general context data
        this_post = get_object_or_404(models.Post, pk=self.kwargs['pk'])  # just gets the post we're currently on
        context['total_upvotes'] = this_post.people_who_upvoted.count()
        context['total_downvotes'] = this_post.people_who_downvoted.count()
        
        if self.request.user.is_authenticated:
            this_person_upvoted_it = this_post.people_who_upvoted.filter(user=self.request.user).count()
            context['this_person_upvoted_it'] = this_person_upvoted_it
            this_person_downvoted_it = this_post.people_who_downvoted.filter(user=self.request.user).count()
            context['this_person_downvoted_it'] = this_person_downvoted_it
        return context

        


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = forms.PostForm
    model = models.Post
    # fields = ('title', 'message', 'city', 'video')
    template_name = "posts/post_form.html"

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    # the success_url will be the get_absolute_url from models.py


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "city")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

# class UserPage(generic.ListView):
    
    
    
def UpvoteView(request, pk):
    # post = get_object_or_404(models.Post, id=request.POST.get('post_id'))
    # post.upvotes.add(request.user)
    # request.user.profile.upvoted_posts.add(post)
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))
    upvote, created = Upvote.objects.get_or_create(user=request.user, post=post)
    if post.people_who_downvoted.filter(user=request.user).count() > 0:
        for x in post.people_who_downvoted.filter(user=request.user):
            x.delete()
            
    if not created:
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={'pk': pk, 'username': post.user.username}))
    else:
        upvote.post = post
        upvote.user = request.user
        upvote.save()
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={'pk': pk, 'username': post.user.username}))

def DownvoteView(request, pk):
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))
    downvote, created = Downvote.objects.get_or_create(user=request.user, post=post)
    # if post.people_who_upvoted.filter(user=self.request.user).exists():
    if post.people_who_upvoted.filter(user=request.user).count() > 0:
        for x in post.people_who_upvoted.filter(user=request.user):
            x.delete()
    
    if not created:
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={'pk': pk, 'username': post.user.username}))
    else:
        downvote.post = post
        downvote.user = request.user
        downvote.save()
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={'pk': pk, 'username': post.user.username}))

