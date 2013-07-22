# Create your views here.
from django.views.generic.detail import DetailView
from dirapp.models import UserProfile
from dirapp.forms import LoginForm, UserProfileForm, UserForm, PassForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def IndexView(request):
    # Search logic
    q = request.GET.get('q')
    if q is None:
        q = ''
    users_list = UserProfile.objects.search(q)
    # Paginator logic
    paginator = Paginator(users_list, 8) # Pagination by 8 users
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        results = paginator.page(paginator.num_pages)
    return render(request, 'dirapp/userprofile_list.html', {'q': q, 'object_list': results, 'viewname': 'search'})


class PersonDetail(DetailView):
    model = UserProfile


def mylogin(request):
    form = LoginForm(data=request.POST)
    errors = []
     # https://docs.djangoproject.com/en/1.5/topics/auth/default/#how-to-log-a-user-in
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.POST['next'])
            else:
                errors.append('Account disabled!')
        else:
            errors.append('Invalid login!')
    return render(request,'dirapp/login.html', {'form': form, 'errors': errors, 'next': request.GET['next'],
                                                'viewname': 'login'})

def mylogout(request):
    logout(request)
    return redirect(request.GET['next'])

@login_required(login_url=reverse_lazy('dirapp:login'))
def EditProfile(request):
    profile = UserProfile.objects.get(user=request.user)
    userprofile = User.objects.get(username=request.user)
    notice = ''
    if request.method == 'POST':
        passform = PassForm(request.POST, prefix='pass')
        form = UserProfileForm(request.POST, request.FILES, instance=profile, prefix='profile')
        userform = UserForm(request.POST, instance=userprofile, prefix='user')
        if form.is_valid() and userform.is_valid():
            form.save()
            userform.save()
        if passform.is_valid():
            password = passform.cleaned_data['passA']
            if password != '':
                user = request.user
                user.set_password(password)
                user.save()
                notice = 'Password changed succesfully!'
    else:
        form = UserProfileForm(instance=profile,prefix='profile')
        userform = UserForm(instance=userprofile,prefix='user')
        passform = PassForm(prefix='pass')
    return render(request, 'dirapp/userprofile_edit.html', {'form': form, 'userform': userform, 'passform': passform,
                                                            'notice': notice, 'viewname':'profile' })