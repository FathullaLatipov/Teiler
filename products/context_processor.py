from products.models import CategoryModel, ProductModel, BrandModel


def product_categories(request):
    categories = CategoryModel.objects.order_by('pk')
    products = ProductModel.objects.order_by('pk')
    brands = BrandModel.objects.order_by('pk')

    return {
        'categories': categories,
        'products': products,
        'brands': brands
    }
