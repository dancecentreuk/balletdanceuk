from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from .forms import CreateBlogForm

from .models import *
from django.views.generic import DetailView, ListView, CreateView


class BlogListingDetail(DetailView):
    template_name = 'blogs/blog-detail.html'
    model = BlogPost
    context_object_name = 'listing'

    def get_context_data(self, *args, **kwargs):
        context = super(BlogListingDetail, self).get_context_data(**kwargs)
        context['blog_listings'] = BlogPost.objects.filter(is_allowed=True)
        return context


class BlogListingsView(ListView):
    model = BlogPost
    template_name = 'blogs/blog-listing.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_posting=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BlogListingsView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # context['location_choices'] = location_choices
        return context


@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateBlogView(SuccessMessageMixin, CreateView):
    model = BlogPost
    template_name = 'blogs/create-blog.html'
    form_class = CreateBlogForm
    success_url = '/'
    success_message = 'Your blog has been succesfully created'

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        return super(CreateBlogView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog-detail', kwargs={'pk': self.object.id})

class CategoryDetailView(ListView):
    model = BlogPost
    template_name = 'blogs/category-detail.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return BlogPost.objects.filter(category=self.category).filter(is_allowed=True)


    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context