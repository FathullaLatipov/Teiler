from products.models import CategoryModel


def product_categories(request):
    categories = CategoryModel.objects.order_by('pk')

    return {
        'categories': categories,
    }
