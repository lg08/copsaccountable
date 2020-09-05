from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404, render
from posts.models import Upvote, Downvote
from django.urls import reverse
from django.utils.text import slugify
from . import forms
from .models import Post, Comment
from cities.models import City, State
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        object_list = Post.objects.all()[0:30]
        return object_list

class PostDetail(generic.DetailView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # general context data
        this_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['total_upvotes'] = this_post.people_who_upvoted.count()
        context['total_downvotes'] = this_post.people_who_downvoted.count()
        context['comment_form'] = forms.CommentForm()

        if self.request.user.is_authenticated:
            this_person_upvoted_it = this_post.people_who_upvoted.filter(
                user=self.request.user).count()
            context['this_person_upvoted_it'] = this_person_upvoted_it
            this_person_downvoted_it = this_post.people_who_downvoted.filter(
                user=self.request.user).count()
            context['this_person_downvoted_it'] = this_person_downvoted_it

            context['current_user'] = self.request.user
        return context


def create_comment(request, postpk, commentpk, subcomment):
    post = get_object_or_404(Post, pk=postpk)
    if request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if subcomment == 1:  # it's a subcomment
                new_comment.comment = get_object_or_404(Comment, pk=commentpk)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
    return HttpResponseRedirect(reverse('posts:detail',
                                        kwargs={
                                            'pk': postpk,
                                        }))


def form_create_view(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post()
            new_post.state = State.objects.get(
                slug=slugify(form.cleaned_data['state']))
            new_post.city = City.objects.get(
                slug=slugify(form.cleaned_data['city']),
                state=new_post.state)
            new_post.title = form.cleaned_data['title']
            new_post.message = form.cleaned_data['message']
            new_post.user = request.user
            new_post.time_information = form.cleaned_data['time_information']
            new_post.location_information = form.cleaned_data['location_information']
            new_post.video = form.cleaned_data['video']
            new_post.thumbnail = form.cleaned_data['thumbnail']
            new_post.save()
            return HttpResponseRedirect(reverse('posts:detail', kwargs={
                'pk': new_post.pk,
            }))
    else:
        form = forms.PostForm()
    context = {
        'form': form,
        }
    return render(request, 'posts/post_form.html', context)


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("home")
    template_name = 'posts/post_confirm.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


class UserPage(generic.ListView):
    model = Post
    template_name = "posts/user_page.html"

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


def UpvoteView(request, pk):
    # post = get_object_or_404(models.Post, id=request.POST.get('post_id'))
    # post.upvotes.add(request.user)
    # request.user.profile.upvoted_posts.add(post)
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    upvote, created = Upvote.objects.get_or_create(
        user=request.user, post=post)
    if post.people_who_downvoted.filter(user=request.user).count() > 0:
        for x in post.people_who_downvoted.filter(user=request.user):
            x.delete()
            post.num_of_downvotes -= 1
            post.save()

    if not created:
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={
                                                'pk': pk,
                                            }))
    else:
        upvote.post = post
        upvote.user = request.user
        upvote.save()
        post.num_of_upvotes += 1
        post.save()
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={
                                                'pk': pk,
                                            }))


def DownvoteView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    downvote, created = Downvote.objects.get_or_create(
        user=request.user,
        post=post)
    # deletes your previous upvote if you did this
    if post.people_who_upvoted.filter(user=request.user).count() > 0:
        for x in post.people_who_upvoted.filter(user=request.user):
            x.delete()
            post.num_of_upvotes -= 1
            post.save()

    if not created:
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={
                                                'pk': pk,
                                            }))
    else:
        downvote.post = post
        downvote.user = request.user
        downvote.save()
        post.num_of_downvotes += 1
        post.save()
        return HttpResponseRedirect(reverse('posts:detail',
                                            kwargs={
                                                'pk': pk,
                                            }))


class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'posts/search_results.html'
    context_object_name = "search_results_list"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(message__icontains=query) |
            Q(state__name__icontains=query) |
            Q(city__name__icontains=query) |
            Q(location_information__icontains=query) |
            Q(time_information__icontains=query)
        )
        return object_list


class WorstPostsView(generic.ListView):
    model = Post
    template_name = 'posts/worst_posts_list.html'
    context_object_name = 'worst_posts_list'

    def get_queryset(self):
        object_list = Post.objects.order_by('-num_of_downvotes')[0:30]
        return object_list


class BestPostsView(generic.ListView):
    model = Post
    template_name = 'posts/best_posts_list.html'
    context_object_name = 'worst_posts_list'

    def get_queryset(self):
        object_list = Post.objects.order_by('-num_of_upvotes')[0:30]
        return object_list
