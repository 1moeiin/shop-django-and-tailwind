from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Post
from .cart import Cart
from django.http import JsonResponse

# Create your views here.

@require_POST
def add_to_cart(request, product_id):
    try:
        quantity = request.POST['quantity']
        cart = Cart(request)
        product = get_object_or_404(Post, id=product_id)

        for _ in range(int(quantity)):
            cart.add(product)

        cart_quantity = cart.cart[str(product_id)]['quantity']

        if product.inventory == cart_quantity:
            count = True
        else:
            count = False
        
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'cart_count': count,
        }
        return JsonResponse(context)
    except:
        return JsonResponse({"error": "Invalid request."})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
