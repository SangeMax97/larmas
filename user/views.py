# user/views.py
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect

class SignUp(generic.CreateView):
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    redirect_authenticated_user = False
    
    
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


class Profile(generic.TemplateView):
    template_name = 'user/profile.html'
    redirect_authenticated_user = False
    
    def dispatch(self, request, *args, **kwargs):
        print
        if self.redirect_authenticated_user and not self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


def edit_profile(request):
    if(request.method=='POST'):
        
        user = User.objects.get(email=request.user)
        user.first_language  = request.POST.get('first_language', '')
        user.second_language = request.POST.get('second_language', '')
        user.third_language  = request.POST.get('third_language', '')
        user.first_name      = request.POST.get('first_name', '')
        user.last_name       = request.POST.get('last_name', '')
        user.gender          = request.POST.get('gender', '')
        user.email           = request.POST.get('email', '')
        age                  = request.POST.get('age', '')
        if( age == ''):
            user.age = 0
        else:
            user.age = int(age)       

        user.save()

    return render(request, 'user/profile.html')


