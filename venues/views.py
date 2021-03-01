from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
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

    # def get_success_url(self):
    #     return reverse('jobs:single-listing', kwargs={'slug': self.object.slug, 'pk': self.object.id})


