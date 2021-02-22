from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from courses.models import WeeklyBalletClass, Level
from users.models import DancersProfile, Account, DancerImage
from jobs.models import Listing
from datetime import date
from django.utils.timezone import now
from .choices import location_choices, age_choices, gender_choices


class HomeView(ListView):
    template_name = 'pages/index.html'
    context_object_name = 'courses'
    model = WeeklyBalletClass
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        context['talents'] = DancersProfile.objects.order_by("-pk")
        context['listings'] = Listing.objects.filter(is_posting=True).order_by('-pk')
        context['postings'] = Listing.objects.filter(is_posting=False).order_by('date')
        context['classes_count'] = WeeklyBalletClass.objects.all().count()
        return context


# def age_range(min_age, max_age):
#     current = now().date()
#     min_date = date(current.year - min_age, current.month, current.day)
#     max_date = date(current.year - max_age, current.month, current.day)
#
#     return user_profiles.filter(birthdate__gte=max_date,
#                                 birthdate__lte=min_date).order_by("birthdate")


class TalentListView(ListView):
    template_name = 'pages/talent.html'
    context_object_name = 'talents'
    model = DancersProfile
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super(TalentListView, self).get_context_data(**kwargs)
        context['location_choices'] = location_choices
        context['age_choices'] = age_choices
        context['gender_choices'] = gender_choices
        return context

class TalentDetailView(DetailView):
    template_name = 'pages/talent-detail.html'
    model = DancersProfile
    context_object_name = 'talent'


    def get_context_data(self, **kwargs):
        context = super(TalentDetailView, self).get_context_data(**kwargs)
        dance_profile = get_object_or_404(DancersProfile, pk=self.kwargs['pk'])
        author = dance_profile.user.id
        context['courses'] = WeeklyBalletClass.objects.filter(author_id=author)
        context['images'] = DancerImage.objects.filter(owner=dance_profile)
        return context


def searchTalent(request):

    queryset_list = DancersProfile.objects.all()


    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            queryset_list = queryset_list.filter(bio__icontains=keyword)


    if 'gender' in request.GET:
        gender = request.GET['gender']
        if gender:
            queryset_list = queryset_list.filter(user__profile__gender=gender)


    if 'age_group' in request.GET:
        age = request.GET['age_group']
        if age:
            queryset_list = queryset_list.filter(age_group=age)

    if 'talent_location' in request.GET:
        location = request.GET['talent_location']
        if location:
            queryset_list = queryset_list.filter(user__profile__location=location)

    paginator = Paginator(queryset_list, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'talents': paged_listings,
        'gender_choices':gender_choices,
        'location_choices':location_choices,
        'age_choices': age_choices,
        'values': request.GET

    }

    return render(request, 'pages/talent-search.html', context)
