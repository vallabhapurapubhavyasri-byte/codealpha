def cart_total_items(request):
    """
    Context processor that makes the total number of items in the cart
    available to all templates (so the navbar badge is always up to date).
    """
    cart = request.session.get('cart', {})
    total_count = sum(cart.values())
    return {'cart_total_items': total_count}
