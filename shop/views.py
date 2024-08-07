from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.

def main(request):
    return render(request, "shop/index.html")

def disable_account(request):
    return render(request, "shop/disabel_account.html")

def products_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Post.published.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    pagination = Paginator(products, 4)
    page_number = request.GET.get('page', 1)
    
    try:
        products = pagination.page(page_number)
    except EmptyPage:
        products = pagination.page(pagination.num_pages)
    except PageNotAnInteger:
        products = pagination.page(1)
    
    context = {
        'products': products,
        'category': category,
        'categories': categories,
    }
    
    return render(request, "shop/product_list.html", context)


@login_required
def product_details(request, pk, slug):
    product = get_object_or_404(Post, slug=slug, id=pk, status=Post.Status.PUBLISHED)
    comments = product.comments.filter(active=True)
    form = CommentForm()
    context = {
        'product': product,
        'form': form, 
        'comments': comments,
    }
    
    return render(request, "shop/product_detail.html", context)

@login_required
def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'], cd['message'], "tuningartperformance@gmail.com", ["amomoeiin@gmail.com"], fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    
    return render(request, "forms/ticket.html", {'form': form, 'sent': sent})


@require_POST
def product_comment(request, product_id, product_slug):
    
    product = get_object_or_404(Post, slug=product_slug, id=product_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
        return redirect('shop:main')
    
    context = {
        'product': product,
        'form': form,
        'comment': comment,
    }
    
    return render(request, "forms/comment.html", context)


def search_post(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = Post.published.filter(description__icontains=query)
            results2 = Post.published.filter(title__icontains=query)
            results = results1 | results2
        
    context = {
        'query': query,
        'results': results,
    }
        
    return render(request, 'forms/search.html', context)


# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('shop:index')
#                 else:
#                     return redirect('shop:disable_account')
                
#             else:
#                 return redirect('shop:disable_account')
            
#     else:
#         form = LoginForm()
    
#     return render(request, 'forms/login.html', {'form': form})    


def log_out(request):
    logout(request)
    return redirect('shop:main')


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegister()
    
    return render(request, 'registration/register.html', {'form': form})