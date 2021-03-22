from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import WeeklyBalletClass, Level, CourseReview
from .forms import CreateCoursesForm, UpdateCourseForm, CourseReviewForm
from pages.choices import location_choices, course_level_choices, age_choices, day_choices



def add_course_review(request):
    pass

@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateCourseReview(CreateView):
    model = CourseReview
    template_name = 'courses/create-course_review.html'
    form_class = CourseReviewForm

    def get(self, request, *args, **kwargs):
        self.course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
        # if not request.user.is_authenticated:
        #     messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
        #     return HttpResponseRedirect('/jobs/')
        return super(CreateCourseReview, self).get(request, *args, **kwargs)



    def form_valid(self, form):
        course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
        form = form.save(commit=False)
        form.user = self.request.user
        form.course = course
        form.save()
        return super(CreateCourseReview, self).form_valid(form)


    def get_context_data(self, *args, **kwargs):
        context = super(CreateCourseReview, self).get_context_data(*args, **kwargs)
        self.course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
        context['course'] = self.course
        return context


    def get_success_url(self):
        self.course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
        return reverse('courses:course-detail', kwargs={'pk': self.course.pk, 'slug': self.course.slug})








class CoursesView(ListView):
    model = WeeklyBalletClass
    template_name = 'courses/course-list.html'
    paginate_by = 10
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        context['age_choices'] = age_choices
        context['location_choices'] = location_choices
        return context

class SingleCourseView(DetailView):
    template_name = 'courses/single-course.html'
    model = WeeklyBalletClass
    context_object_name = 'course'

    def get_context_data(self, *args, **kwargs):
        context = super(SingleCourseView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        # course = get_object_or_404(CourseReview, course_id=self.kwargs['pk'])
        context['ratings'] = CourseReview.objects.filter(course_id=self.kwargs['pk'])
        return context


@method_decorator(login_required(login_url='/'), name='dispatch')
class CreateCourseView(SuccessMessageMixin, CreateView):
    model = WeeklyBalletClass
    template_name = 'courses/create-course.html'
    form_class = CreateCoursesForm
    success_url = '/'
    success_message = 'Your job has been succesfully created'

    def form_valid(self, form):
        courses = form.save(commit=False)
        courses.author = self.request.user
        courses.save()
        return super(CreateCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse('courses:course-detail', kwargs={'pk': self.object.id, 'slug': self.object.slug})


@method_decorator(login_required(login_url='/'), name='dispatch')
class UpdateCourseView(SuccessMessageMixin, UpdateView):
    model = WeeklyBalletClass
    template_name = 'courses/update-course.html'
    form_class = UpdateCourseForm
    success_message = 'You have successfully updated your job !'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateCourseView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
            return HttpResponseRedirect('/jobs/')
        return super(UpdateCourseView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('courses:course-detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})






class CourseLevelDetailView(ListView):
    model = WeeklyBalletClass
    template_name = 'courses/level-detail.html'
    context_object_name = 'courses'
    paginate_by = 2

    def get_queryset(self):
        self.level = get_object_or_404(Level, pk=self.kwargs['pk'])
        return WeeklyBalletClass.objects.filter(course_level=self.level).filter(is_allowed=True)


    def get_context_data(self, *args, **kwargs):
        context = super(CourseLevelDetailView, self).get_context_data(*args, **kwargs)
        self.level = get_object_or_404(Level, pk=self.kwargs['pk'])
        context['levels'] = Level.objects.all()
        context['level'] = self.level
        context['age_choices'] = age_choices
        context['location_choices'] = location_choices
        return context


def searchCourse(request):

    queryset_list = WeeklyBalletClass.objects.all()


    if 'age_group' in request.GET:
        age = request.GET['age_group']
        if age:
            queryset_list = queryset_list.filter(age_group=age)

    if 'course_level' in request.GET:
        level = request.GET['course_level']
        if level:
            queryset_list = queryset_list.filter(course_level=level)

    if 'course_location' in request.GET:
        location = request.GET['course_location']
        if location:
            queryset_list = queryset_list.filter(location=location)

    paginator = Paginator(queryset_list, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'courses': paged_listings,
        'levels':Level.objects.all().order_by('title'),
        'location_choices':location_choices,
        'age_choices': age_choices,
        'values': request.GET

    }

    return render(request, 'courses/search.html', context)




@method_decorator(login_required(login_url='/'), name='dispatch')
class UpdateCourseReview(UpdateView):
    model = CourseReview
    template_name = 'courses/create-course_review.html'
    form_class = CourseReviewForm

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(CourseReview, pk=self.kwargs['pk'])
        if self.object.user != request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your Review to update !!!')
            return HttpResponseRedirect('/')
        return super(UpdateCourseReview, self).get(request, *args, **kwargs)



    # def form_valid(self, form):
    #     course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
    #     form = form.save(commit=False)
    #     form.user = self.request.user
    #     form.course = course
    #     form.save()
    #     return super(CreateCourseReview, self).form_valid(form)


    def form_valid(self, form):
        return super(UpdateCourseReview, self).form_valid(form)




    # def get_context_data(self, *args, **kwargs):
    #     context = super(CreateCourseReview, self).get_context_data(*args, **kwargs)
    #     self.course = get_object_or_404(WeeklyBalletClass, pk=self.kwargs['pk'])
    #     context['course'] = self.course
    #     return context
    #
    #
    def get_success_url(self):
        dance_course = get_object_or_404(WeeklyBalletClass, pk=self.object.course.id)
        return reverse('courses:course-detail', kwargs={'pk': dance_course.pk, 'slug': dance_course.slug})




