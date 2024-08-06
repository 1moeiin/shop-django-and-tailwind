from django import template
from shop.models import Post, Comment

register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.inclusion_tag("partials/lastest_posts.html")
def lastest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    
    context = {
        'l_posts': l_posts,
    }
    
    return context
