from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from mail.models import Conversation, Communication
from .models import Listing, Category
from.forms import *
from pages.choices import location_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from users.models import  Account


# Create your views here.

class ListingView(ListView):
    template_name = 'jobs/listings.html'
    model = Listing
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        queryset = Listing.objects.filter(is_posting=True)
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(ListingView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['location_choices'] = location_choices
        return context





@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateListingView(SuccessMessageMixin, CreateView):
    model = Listing
    template_name = 'jobs/create-listing.html'
    form_class = CreateListingForm
    success_url = '/'
    success_message = 'Your job has been succesfully created'
    
    
    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.author = self.request.user
        listing.save()
        return super(CreateListingView, self).form_valid(form)

    def get_success_url(self):
        return reverse('jobs:single-listing',  kwargs={'slug': self.object.slug, 'pk': self.object.id})


class SingleListingView(DetailView):
    template_name = 'jobs/single-listing.html'
    model = Listing
    context_object_name = 'listing'

    def get_context_data(self, *args, **kwargs):
        context = super(SingleListingView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



    def post(self, *args, **kwargs):
        user = self.request.user

        if self.request.method == 'POST':
            title = self.request.POST['title']
            sender = user
            recipient = self.request.POST['recipient']
            content = self.request.POST['content']

            recipient = Account.objects.get(id=recipient)

            print(content)

            conversation = Conversation.objects.create(title=title, messenger_1=sender, messenger_2=recipient)

            conversation_id = conversation.id

            communication = Communication(content=content,
                                          sender=sender,
                                          recipient=recipient,
                                          conversation_id=conversation_id
                                          )
            communication.save()
            return redirect('/')

class CategoryListingsView(ListView):
    model = Listing
    template_name = 'jobs/category-detail.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Listing.objects.filter(category=self.category).filter(is_posting=True)



    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListingsView, self).get_context_data(*args, **kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context



def search(request):

    queryset_list = Listing.objects.all().filter(is_posting=True)


    if 'job_title' in request.GET:
        job_title = request.GET['job_title']
        if job_title:
            queryset_list = queryset_list.filter(title__icontains=job_title)

    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            queryset_list = queryset_list.filter(category=job_type)

    if 'job_location' in request.GET:
        location = request.GET['job_location']
        if location:
            queryset_list = queryset_list.filter(location=location)

    paginator = Paginator(queryset_list, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'listings': paged_listings,
        'categories':Category.objects.all().order_by('title'),
        'location_choices':location_choices,
        'values': request.GET

    }

    return render(request, 'jobs/search.html', context)


def searchPosting(request):

    queryset_list = Listing.objects.filter(is_posting=False)


    if 'job_title' in request.GET:
        job_title = request.GET['job_title']
        if job_title:
            queryset_list = queryset_list.filter(title__icontains=job_title)

    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            queryset_list = queryset_list.filter(category=job_type)

    if 'job_location' in request.GET:
        location = request.GET['job_location']
        if location:
            queryset_list = queryset_list.filter(location=location)

    paginator = Paginator(queryset_list, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'listings': paged_listings,
        'categories':Category.objects.all().order_by('title'),
        'location_choices':location_choices,
        'values': request.GET

    }

    return render(request, 'jobs/search-postings.html', context)


class UpdateListingView(SuccessMessageMixin, UpdateView):
    model = Listing
    template_name = 'jobs/update-listing.html'
    form_class = UpdateListingForm
    success_message = 'You have successfully updated your job !'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateListingView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
            return HttpResponseRedirect('/jobs/')
        return super(UpdateListingView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('jobs:single-listing', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class DeleteListingView(SuccessMessageMixin, DeleteView):
    model = Listing
    success_url = '/'
    template_name = 'jobs/delete-listing.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
            return HttpResponseRedirect('/jobs/')
        return super(DeleteListingView, self).get(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Your message has been deleted !!!')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to delete !!!')
            return HttpResponseRedirect(self.success_url)


class PostingView(ListView):
    template_name = 'jobs/postings.html'
    model = Listing
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        queryset = Listing.objects.filter(is_posting=False).order_by('date')
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(PostingView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['location_choices'] = location_choices
        return context


@method_decorator(login_required(login_url='/'), name='dispatch')
class CreatePostingView(SuccessMessageMixin, CreateView):
    model = Listing
    template_name = 'jobs/create-posting.html'
    form_class = CreatePostingForm
    success_url = '/'
    success_message = 'Your job has been succesfully created'

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.author = self.request.user
        listing.is_posting = False
        listing.save()
        return super(CreatePostingView, self).form_valid(form)

    def get_success_url(self):
        return reverse('jobs:single-posting', kwargs={'slug': self.object.slug, 'pk': self.object.id})


class UpdatePostingView(SuccessMessageMixin, UpdateView):
    model = Listing
    template_name = 'jobs/update-posting.html'
    form_class = UpdatePostingForm
    success_message = 'You have successfully updated your job !'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdatePostingView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
            return HttpResponseRedirect('/jobs/')
        return super(UpdatePostingView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('jobs:single-listing', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class SinglePostingView(DetailView):
    template_name = 'jobs/single-posting.html'
    model = Listing
    context_object_name = 'listing'

    def get_context_data(self, *args, **kwargs):
        context = super(SinglePostingView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryPostingsView(ListView):
    model = Listing
    template_name = 'jobs/category-postings.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Listing.objects.filter(category=self.category).filter(is_posting=False).order_by('date')

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryPostingsView, self).get_context_data(*args, **kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class LocationPostingsView(ListView):
    model = Listing
    template_name = 'jobs/location-postings.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        self.location = self.kwargs['location']
        return Listing.objects.filter(location=self.location).filter(is_posting=False).order_by('date')



    def get_context_data(self, *args, **kwargs):
        context = super(LocationPostingsView, self).get_context_data(*args, **kwargs)
        self.location = self.kwargs['location']
        context['categories'] = Category.objects.all()
        context['location'] = self.location
        return context



class LocationListingsView(ListView):
    model = Listing
    template_name = 'jobs/location-listings.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        # self.location = get_object_or_404(Listing, location=self.kwargs['location'])
        self.location = self.kwargs['location']
        return Listing.objects.filter(location=self.location).filter(is_posting=True)



    def get_context_data(self, *args, **kwargs):
        context = super(LocationListingsView, self).get_context_data(*args, **kwargs)
        # self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        self.location = self.kwargs['location']
        context['categories'] = Category.objects.all()
        context['location'] = self.location
        return context

