from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Venue, Category
from pages.choices import location_choices

from .forms import *
# Create your views here.



class VenuesView(ListView):
    template_name = 'venues/venue-listings.html'
    model = Venue
    context_object_name = 'listings'
    paginate_by = 10

    def get_queryset(self):
        queryset = Venue.objects.filter(is_allowed=True)
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(VenuesView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['location_choices'] = location_choices
        return context


class SingleVenueView(DetailView):
    template_name = 'venues/single-venue.html'
    model = Venue
    context_object_name = 'venue'

    def get_context_data(self, *args, **kwargs):
        context = super(SingleVenueView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required(login_url='/'), name='dispatch')
class AddVenueView(SuccessMessageMixin, CreateView):
    model = Venue
    template_name = 'venues/add-venue.html'
    form_class = AddVenueForm
    success_url = '/'
    success_message = 'Your job has been succesfully created'

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.author = self.request.user
        listing.save()
        return super(AddVenueView, self).form_valid(form)

    def get_success_url(self):
        return reverse('venues:venue-detail', kwargs={'pk': self.object.id})


class UpdateVenueView(SuccessMessageMixin, UpdateView):
    model = Venue
    template_name = 'venues/update-venue.html'
    form_class = UpdateVenueForm
    success_message = 'Venue details have successfully been updated !'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateVenueView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
            return HttpResponseRedirect('/jobs/')
        return super(UpdateVenueView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('venues:venue-detail', kwargs={'pk': self.object.pk})


class DeleteVenueView(SuccessMessageMixin, DeleteView):
    model = Venue
    success_url = '/'
    template_name = 'venues/delete-listing.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your listing to update !!!')
            return HttpResponseRedirect('/venues/')
        return super(DeleteVenueView, self).get(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Your venue listing has been deleted !!!')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your venue listing to delete !!!')
            return HttpResponseRedirect(self.success_url)