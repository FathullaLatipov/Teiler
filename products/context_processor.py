from carousel.models import CarouselModel
from help.models import HelpCategory, HelpSubcategory
from products.models import CategoryModel, ProductModel, BrandModel, ColorModel


def product_categories(request):
    categories = CategoryModel.objects.order_by('pk')
    products = ProductModel.objects.order_by('pk')
    brands = BrandModel.objects.order_by('pk')
    colors = ColorModel.objects.order_by('pk')
    carousels = CarouselModel.objects.order_by('pk')
    help_categories = HelpCategory.objects.order_by('pk')
    help_subcategories = HelpSubcategory.objects.order_by('pk')
    random_products = ProductModel.objects.order_by('?')

    return {
        'categories': categories,
        'products': products,
        'brands': brands,
        'colors': colors,
        'carousels': carousels,
        'help_categories': help_categories,
        'help_subcategories': help_subcategories,
        'random_products': random_products
    }
