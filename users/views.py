from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Profile, DancersProfile, Account, CompanyProfile, DancerImage
from jobs.models import Listing
from courses.models import WeeklyBalletClass
from pages.choices import location_choices, gender_choices

from .forms import AccountRegisterForm, UserUpdateForm, DancersUpdateForm, CompanyUpdateForm, AccountProfileForm, \
    DancerImageForm


# Create your views here.

# class UserRegisterView(SuccessMessageMixin, CreateView):
#     template_name = 'users/user-register.html'
#     form_class = AccountRegisterForm
#     form_class_2 = AccountProfileForm
#     success_url = '/'
#     success_message = 'Your User account has been created'
#
#
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user_type = form.cleaned_data['user_types']
#         if user_type == 'is_dancer':
#             user.is_dancer = True
#         elif user_type == 'is_employer':
#             user.is_employer = True
#
#         user.save()
#
#         return redirect(self.success_url)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserRegisterView, self).get_context_data(**kwargs)
#         context['profile_form'] = AccountProfileForm
#         return context


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register-user2.html'
    form_class = AccountRegisterForm
    success_url = '/'
    success_message = 'Your User account has been created'

    def form_valid(self, form):
        user = form.save(commit=False)
        location = form.cleaned_data['location']
        date_of_birth = form.cleaned_data['date_of_birth']
        gender = form.cleaned_data['gender']
        user_type = form.cleaned_data['user_types']
        if user_type == 'is_dancer':
            user.is_dancer = True
        elif user_type == 'is_employer':
            user.is_employer = True
        user._location = location
        user._gender = gender
        user._date_of_birth = date_of_birth

        user.save()

        return redirect(self.success_url)

    def get_context_data(self, *args, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        return context


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class ProfileView(UpdateView):
    template_name = 'users/profile.html'
    model = Account
    context_object_name = 'candidate'
    form_class = DancersUpdateForm
    form_class_2 = UserUpdateForm
    form_class_3 = CompanyUpdateForm
    form_class_4 = DancerImageForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.add_message(self.request, messages.WARNING, 'This is not your profile !')
            return HttpResponseRedirect('/')
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_id = get_object_or_404(Profile, user_id=self.object.pk)
        context['users_form'] = self.form_class_2(instance=user_id)
        context['listings'] = Listing.objects.filter(author=self.object.pk)
        context['courses'] = WeeklyBalletClass.objects.filter(author=self.object.pk)
        if self.request.user.has_dancers_profile():
            dancer_id = get_object_or_404(DancersProfile, user_id=self.object.pk)
            context['form'] = self.form_class(instance=dancer_id)
            context['photo_form'] = self.form_class_4(instance=dancer_id)
            context['images'] = DancerImage.objects.filter(owner=dancer_id)
        if self.request.user.has_company_profile():
            company_id = get_object_or_404(CompanyProfile, user_id=self.object.pk)
            context['company_form'] = self.form_class_3(instance=company_id)


        return context

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.request.user.has_company_profile():
    #         pass
    #     if not self.request.has_dancers_profile():
    #         pass
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'dancerscope' in self.request.POST:
            form = DancersUpdateForm(self.request.POST, self.request.FILES, instance=self.object.dancers_profile)
            if form.is_valid():
                form.save()
                messages.add_message(self.request, messages.SUCCESS, 'You have succesfully update your dancers info !')
                return super(ProfileView, self).form_valid(form)
        elif 'companycope' in self.request.POST:
            form = CompanyUpdateForm(self.request.POST, self.request.FILES, instance=self.object.company_profile)
            if form.is_valid():
                form.save()
                messages.add_message(self.request, messages.SUCCESS, 'You have succesfully update your company info !')
                return super(ProfileView, self).form_valid(form)
        elif 'dancerImage' in self.request.POST:
            form = DancerImageForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.owner = self.object.dancers_profile
                data.save()
                messages.add_message(self.request, messages.SUCCESS, 'You have succesfully added am image')
                return super(ProfileView, self).form_valid(form)
        else:
            form = UserUpdateForm(self.request.POST, self.request.FILES, instance=self.object.profile)
            if form.is_valid():
                form.save()
                messages.add_message(self.request, messages.SUCCESS, 'You have succesfully update your Profile info !')
                return super(ProfileView, self).form_valid(form)

    def get_success_url(self):
        success_id = self.get_object()
        return reverse('users:profile', kwargs={'pk': success_id.pk})


# class NewProfileView(UpdateView):
#     template_name = 'users/profile.html'
#     model = Account
#     context_object_name = 'candidate'
#     form_class = DancersUpdateForm
#     form_class_2 = UserUpdateForm
#     form_class_3 = CompanyUpdateForm
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super(NewProfileView, self).get(request, *args, **kwargs)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(NewProfileView, self).get_context_data(**kwargs)
#         dancer_id = get_object_or_404(DancersProfile, user_id=self.object.pk)
#         user_id = get_object_or_404(Profile, user_id=self.object.pk)
#         company_id = get_object_or_404(CompanyProfile, user_id=self.object.pk)
#         context['form'] = self.form_class(instance=dancer_id)
#         context['users_form'] = self.form_class_2(instance=user_id)
#         context['company_form'] = self.form_class_3(instance=company_id)
#         return context
#
#     def form_valid(self, form):
#         print(self.request.POST)
#         if 'dope' in self.request.POST:
#             form = DancersUpdateForm(self.request.POST, self.request.FILES, instance=self.object.dancers_profile)
#             if form.is_valid():
#                 form.save()
#                 return super(NewProfileView, self).form_valid(form)
#         elif 'companycope' in self.request.POST:
#             form = CompanyUpdateForm(self.request.POST, self.request.FILES, instance=self.object.company_profile)
#             if form.is_valid():
#                 form.save()
#                 return super(NewProfileView, self).form_valid(form)
#         else:
#             form = UserUpdateForm(self.request.POST, self.request.FILES, instance=self.object.profile)
#             if form.is_valid():
#                 form.save()
#                 return super(NewProfileView, self).form_valid(form)
#
#     def get_success_url(self):
#         success_id = self.get_object()
#         return reverse('users:profile', kwargs={'pk': success_id.pk})

class CreateDancerProfileView(CreateView):
    model = DancersProfile
    form_class = DancersUpdateForm
    template_name = 'users/update.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_dancers_profile():
            messages.add_message(self.request, messages.WARNING, 'You allready have a  dancers profile')
            return redirect('users:profile', request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Your Dance Profile has been Created')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.id})


class CreateCompanyProfileView(CreateView):
    model = CompanyProfile
    form_class = CompanyUpdateForm
    template_name = 'users/update.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_company_profile():
            return redirect('users:profile', request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})

    # return reverse_lazy('detail', kwargs={'pk': kwargs['idnumber']})


class DancerUpdate(UpdateView):
    model = DancersProfile
    success_message = 'You Updated your profile successfully'
    template_name = 'users/update.html'
    form_class = DancersUpdateForm


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    success_message = 'You Updated your profile successfully'
    template_name = 'users/update.html'
    form_class = UserUpdateForm
    dancer_form = DancersUpdateForm

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super(UserUpdateView, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UserUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        user = get_object_or_404(DancersProfile, )
        print(user.user)
        context['user_form'] = self.dancer_form(instance=user)
        return context

    def form_valid(self, form):
        user = get_object_or_404(DancersProfile, )
        user_form = DancersUpdateForm(self.request.POST, self.request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:update-profile', kwargs={'pk': self.object.pk})


def add_photo(request):
    if request.method == 'POST':
        form = DancerImageForm(request.POST, request.FILES or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.owner = request.user
            data.save()
            return redirect('users:profile')
        else:
            HttpResponse(request, 'unable to save your images')


def delete_dancer_photo(request, pk):
    photo = DancerImage.objects.get(id=pk)
    if photo.owner.user == request.user:
        photo.delete()
        messages.success(request, 'Photo has successfully been deleted')
        return redirect('users:profile', request.user.id)
    else:
        messages.error(request, 'Error: not your photo to delete')
        return redirect('/')
