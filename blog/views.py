from django.shortcuts import render , get_object_or_404
from django.utils import timezone
from .models import Post, Product
from .forms import BlogPostForm, BlogSuggestForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    return render(request, "index.html")

def new_product(request):
    return render(request, "index.html")
    
def gallery(request):
    return render(request, "gallery.html")

def post_list(request):
    #GET request checks if there is any additional queries in the string.
    #GET is the HTTP method to access the query.
    #get is the python method to find the dictionary values.
    #'false' here is just the answer to the question in the event that there isn't something to show ie when the question is asked 'is there something here?' , we need an answer, so False is a friendly way to show this
    top = request.GET.get('top', False)
    if top:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views')[:3]
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogtests.html",{'posts':posts})

def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "blogdetail.html", {'post': post})

def top_5(request):
    top5 = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views')[:3]
    return render (request, "top5.html", {'top5': top5} )

def melbourne(request):
    top5 = Post.objects.filter(published_date__lte=timezone.now()).order_by('-views')
    return render (request, "melbourne_gallery.html", {'top5': top5} )

def new_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
           # return render (request, "blogtest.html")
            return redirect('blog.views.post_detail', id = post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blogpostform.html', {'form':form})

def suggestion_post(request):
    if request.method == "POST":
        form = BlogSuggestForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return render (request, "suggest_thanks.html")
    else:
        form = BlogSuggestForm()
    return render(request, 'blogpostform.html', {'form':form})

def edit_post(request,pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method =="POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, id=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html',{'form':form})
    
#set up paypal
@csrf_exempt
def paypal_return(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal_return.html', args)

def paypal_cancel(request):
    args = {'post':request.POST, 'get':request.GET}
    return render( request,'paypal_cancel.html', args)
