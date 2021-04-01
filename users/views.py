from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from .models import Profile, DancersProfile, Account, CompanyProfile, DancerImage
from jobs.models import Listing
from courses.models import WeeklyBalletClass
from blog.models import BlogPost
from venues.models import Venue
from pages.choices import location_choices, gender_choices

from .forms import AccountRegisterForm, UserUpdateForm, DancersUpdateForm, CompanyUpdateForm, AccountProfileForm, \
    DancerImageForm

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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


# class UserRegisterView(SuccessMessageMixin, CreateView):
#     template_name = 'users/register-user2.html'
#     form_class = AccountRegisterForm
#     success_url = '/'
#     success_message = 'Your User account has been created'
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         location = form.cleaned_data['location']
#         date_of_birth = form.cleaned_data['date_of_birth']
#         gender = form.cleaned_data['gender']
#         user_type = form.cleaned_data['user_types']
#         if user_type == 'is_dancer':
#             user.is_dancer = True
#         elif user_type == 'is_employer':
#             user.is_employer = True
#         user._location = location
#         user._gender = gender
#         user._date_of_birth = date_of_birth
#         user.save()
#
#         return redirect(self.success_url)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserRegisterView, self).get_context_data(**kwargs)
#         return context



class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register-user2.html'
    form_class = AccountRegisterForm
    success_url = '/'
    success_message = 'Your User account has been created'

    def form_valid(self,  form):
        user = form.save(commit=False)
        location = form.cleaned_data['location']
        date_of_birth = form.cleaned_data['date_of_birth']
        gender = form.cleaned_data['gender']
        email = form.cleaned_data['email']
        user_type = form.cleaned_data['user_types']
        if user_type == 'is_dancer':
            user.is_dancer = True
        elif user_type == 'is_employer':
            user.is_employer = True
        user._location = location
        user._gender = gender
        user._date_of_birth = date_of_birth
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        domain = get_current_site(self.request).domain
        link = reverse('users:activate', kwargs={
            'uidb64': uidb64, 'token': token_generator.make_token(user)})

        activate_url = 'http://' + domain + link

        email_subject = 'Activate your account'
        email_body = 'Hi ' + user.first_name + ' Ps use the link below to activate your account\n' + activate_url
        email_address = form.cleaned_data.get('email')
        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@dance.com',
            [email_address]

        )

        EmailThread(email).start()
        messages.add_message(self.request, messages.SUCCESS, 'You are now registered ps check your email to activate your account')
        return redirect('users:login')

    def get_context_data(self, *args, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        return context


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('users:login' + '?message=' + 'User allreaedy activated')

            if user.is_active:
                return redirect('users:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account Activated sucessfully')
            return redirect('users:login')

        except Exception as e:
            pass

        return redirect('sign-in')


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
            messages.add_message(self.request, messages.WARNING, ': This is not your profile !')
            return HttpResponseRedirect('/')
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_id = get_object_or_404(Profile, user_id=self.object.pk)
        context['users_form'] = self.form_class_2(instance=user_id)
        context['listings'] = Listing.objects.filter(author=self.object.pk)
        context['blogs'] = BlogPost.objects.filter(featured=True)
        context['courses'] = WeeklyBalletClass.objects.filter(author=self.object.pk)
        context['venues'] = Venue.objects.filter(author=self.object.pk)
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
                messages.add_message(self.request, messages.SUCCESS, ': You have successfully update your dancers info !')
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


class DeleteDancersProfile(DeleteView):
    model = DancersProfile
    success_url = '/'
    template_name = 'users/delete-dancers-profile.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your profile to Delete !!!')
            return HttpResponseRedirect('/')
        return super(DeleteDancersProfile, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Your dancers profile has been deleted !!!')
            return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': self.request.user.id}))
        else:
            messages.add_message(self.request, messages.WARNING, 'Error: We were unable to delete Dancers Profile !!!')
            return HttpResponseRedirect(self.success_url)







    # class DeleteListingView(SuccessMessageMixin, DeleteView):
    #     model = Listing
    #     success_url = '/'
    #     template_name = 'jobs/delete-listing.html'
    #
    #     def get(self, request, *args, **kwargs):
    #         self.object = self.get_object()
    #         if self.object.author != self.request.user:
    #             messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to update !!!')
    #             return HttpResponseRedirect('/jobs/')
    #         return super(DeleteListingView, self).get(request, *args, **kwargs)
    #
    #     def delete(self, request, *args, **kwargs):
    #         self.object = self.get_object()
    #         if self.object.author == self.request.user:
    #             self.object.delete()
    #             messages.add_message(self.request, messages.SUCCESS, 'Your message has been deleted !!!')
    #             return HttpResponseRedirect(self.success_url)
    #         else:
    #             messages.add_message(self.request, messages.WARNING, 'Cheeky not your message to delete !!!')
    #             return HttpResponseRedirect(self.success_url)


class CreateCompanyProfileView(SuccessMessageMixin, CreateView):
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
        messages.add_message(self.request, messages.SUCCESS, 'Your company profile has been created !!!')
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})

class DeleteCompanyProfile(DeleteView):
    model = CompanyProfile
    success_url = '/'
    template_name = 'users/delete-company-profile.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            messages.add_message(self.request, messages.WARNING, 'Cheeky not your Company profile to Delete !!!')
            return HttpResponseRedirect('/')
        return super(DeleteCompanyProfile, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Your Company  profile has been deleted !!!')
            return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': self.request.user.id}))
        else:
            messages.add_message(self.request, messages.WARNING, 'Error: We were unable to delete Company Profile !!!')
            return HttpResponseRedirect(self.success_url)


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
