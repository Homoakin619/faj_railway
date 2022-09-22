from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


from core.models import Post,Profile
from core.forms import CreatePostForm,ProfileForm
from core.mixins import CheckVerificationMixin, StaffAccessMixin


class RedirectPage(LoginRequiredMixin,generic.ListView):
    template_name = 'core/redirect_page.html'
    model = Post

class PostDetail(LoginRequiredMixin,CheckVerificationMixin,generic.DetailView):
    template_name = 'core/content_details.html'
    model = Post
    context_object_name = 'post'

class LoginRegisterView(generic.View):
    templage_name = 'core/login.html'
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request,self.templage_name)

    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        form_type = request.POST.get('form_type')
        if form_type == 'login':
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('dashboard'))
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request,self.templage_name,{'error':'Login credential do not exist'})
        else:
            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request,user)
            return HttpResponseRedirect('/')
        

class HomepageView(LoginRequiredMixin,CheckVerificationMixin,generic.ListView):
    template_name = 'core/index.html'
    
    redirect_url = reverse_lazy('not_verified')
    model = Post
    context_object_name = 'posts'


class AdminDashboardView(LoginRequiredMixin,StaffAccessMixin,generic.ListView):
    template_name = 'core/dashboard.html'
    redirect_url = reverse_lazy('home')
    model = Profile
    context_object_name = 'audience'


class AdminAllPosts(LoginRequiredMixin,StaffAccessMixin,generic.ListView):
    model = Post
    template_name = 'core/all_posts.html'
    context_object_name = 'posts'
     


class AdminEditUserView(LoginRequiredMixin,StaffAccessMixin,generic.View):
    template_name = 'core/edit_user.html'
    redirect_url = reverse_lazy('home')
    def get(self,request,*args,**kwargs):
        user = get_object_or_404(User,pk=kwargs['pk'])
        profile = get_object_or_404(Profile,user=user)
        form = ProfileForm(instance=profile)
        return render(request,self.template_name,{'form':form,'user':user})

    def post(self,request,*args,**kwargs):
        
        user = get_object_or_404(User,pk=kwargs['pk'])
        profile = get_object_or_404(Profile,user=user)
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.user = user
            print(form.user.id)
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
        return self.get(request,*args,**kwargs,form=form)

class AdminAddPostView(LoginRequiredMixin,StaffAccessMixin,generic.View):
    template_name = 'core/create_post.html'
    redirect_url = reverse_lazy('home')
    def get(self,request,*args,**kwargs):
        form = CreatePostForm()
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        context = {'form':form}
        return render(request,self.template_name,context)


class AdminEditPostView(LoginRequiredMixin,StaffAccessMixin,generic.View):
    template_name = 'core/create_post.html'
    redirect_url = reverse_lazy('home')

    def get(self,request,*args,**kwargs):
        query = get_object_or_404(Post,pk=kwargs['pk'])
        form = CreatePostForm(instance=query)
        context = {'form':form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        query = get_object_or_404(Post,pk=kwargs['pk'])
        form = CreatePostForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        context = {'form':form}
        return render(request,self.template_name,context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))