from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login


# Create your views here.

# @login_required(login_url='login')
# def gallery(request):
#     category = request.GET.get('category')
#     if category == None:
#         photos = Photo.objects.all()
#     else:
#         photos = Photo.objects.filter(category__name=category)
#
#     categories = Category.objects.all()
#     context = {'categories': categories, 'photos': photos}
#     return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user  # Get the logged-in user
    category_name = request.GET.get('category')

    if category_name:
        photos = Photo.objects.filter(user=user, category__name=category_name)  # Filter by user and category
    else:
        photos = Photo.objects.filter(user=user)  # Show only user's photos

    categories = Category.objects.filter(user=user)

    context = {
        'categories': categories,
        'photos': photos
    }
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(pk=pk)
    item = get_object_or_404(Photo, pk=pk)
    related_items = Photo.objects.filter(category=photo.category).exclude(pk=pk)[0:3]
    context = {'photo':photo, 'item': item, 'related_items': related_items}


    return render(request, 'photos/photo.html', context)

@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = Category.objects.filter(user=user)  # Only show user's categories

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'], user=user)
        else:
            category = None

        photo = Photo.objects.create(
            user=request.user,
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('gallery')
    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

def base(request):
    return render(request, 'photos/base.html')


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('gallery')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('gallery')
        return super(RegisterPage, self).get(*args, **kwargs)

