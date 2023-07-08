from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, FoodItem
from menu.forms import CategoryForm,FoodItemForm
from vendor.models import Vendor
from django.template.defaultfilters import slugify


def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.Objects.filter(vendor = vendor).order_by('created_at')
    context = {
        'categories' : categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


def fooditems_by_category(request, pk =None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk = pk)    
    fooditems = FoodItem.objects.filter(vendor = vendor, category = category)
    
    context = {
        'category' : category,
        'fooditems' : fooditems,
    }
    
    return render(request, 'vendor/fooditems_by_category.html', context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            vendor = Vendor.objects.get(user=request.user)
            category = form.save(commit = False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Addded sucessfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html',context)

def edit_category(request,pk =None):
    category = get_object_or_404(Category, pk = pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            vendor = Vendor.objects.get(user=request.user)
            category = form.save(commit = False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated sucessfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance= category)
    
    context = {
        'form' : form,
        'category' : category,
    }

    return render(request, 'vendor/edit_category.html')

def delete_category(request, pk = None):
    category = get_object_or_404(Category, pk = pk)
    category.delete()
    messages.success(request, 'Category has been deleted sucessfully!')
    return redirect('menu_builder')


def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = Vendor.objects.get(user = request.user)
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item added successfully!!')
            return redirect('fooditems_by_category', food.category.id)
        
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor = vendor)

    context = {
        'form' : form,
    }
    return render(request, 'vendor/add_food.html',context)

def edit_food(request,pk =None):
    food = get_object_or_404(FoodItem, pk = pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            vendor = Vendor.objects.get(user=request.user)
            food = form.save(commit = False)
            food.vendor = vendor
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item updated sucessfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance= food)
        form.fields['category'].queryset = Category.objects.filter(vendor = vendor)
    
    context = {
        'form' : form,
        'food' : food,
    }

    return render(request, 'vendor/edit_food.html')

def delete_food(request, pk = None):
    food = get_object_or_404(FoodItem, pk = pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted sucessfully!')
    return redirect('fooditems_by_category', food.category.id)