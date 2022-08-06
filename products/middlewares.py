from products import models


def basket_middleware(get_response):
    def middleware(request):
        if 'basket_id' in request.session:
            basket_id = request.session['basket_id']
            basket = models.BasketModel.objects.get(id=basket_id)
            request.basket = basket
        else:
            request.basket = None

        response = get_response(request)
        return response
    return middleware
