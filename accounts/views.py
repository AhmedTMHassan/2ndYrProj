from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .forms import CustomUserCreationForm
from .models import CustomUser, Profile
from django.urls import reverse_lazy


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    

class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    fields = ['username']

class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'