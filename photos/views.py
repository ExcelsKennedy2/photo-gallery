from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo

# Create your views here.

def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(pk=pk)
    item = get_object_or_404(Photo, pk=pk)
    related_items = Photo.objects.filter(category=photo.category).exclude(pk=pk)[0:3]
    context = {'photo':photo, 'item': item, 'related_items': related_items}


    return render(request, 'photos/photo.html', context)

def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('gallery')
    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

def base(request):
    return render(request, 'photos/base.html')