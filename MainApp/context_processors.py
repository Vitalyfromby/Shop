from .models import Category

def sidebar(request):
    categories = Category.objects.all()
    return {'categories': categories}