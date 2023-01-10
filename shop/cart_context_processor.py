from shop.models import ShopCart



def get_cart(request):
    try:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
        return{
            "carts":carts,
            "total":total,
            "total_quantity":total_quantity,
        }
    except:
        return{
            "carts":None,
            "total":0,
            "total_quantity":0,
        }