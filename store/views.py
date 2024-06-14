from django.shortcuts import get_object_or_404, render

from .models import Item, ItemTag
from .paginator import paginator


def store(request):
    items = Item.objects.filter(is_available=True)
    context = {
        'page_obj': paginator(request, items, 9),
        'range': [*range(1)],  
    }

    return render(request, 'store/main_page.html', context)


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {
        'item': item,
    }
    return render(request, 'store/item_details.html', context)


def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])
    context = {
        'tag': tag,
        'page_obj': paginator(request, items, 3),
    }
    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    tags = ItemTag.objects.all()
    context = {
        'page_obj': paginator(request, tags, 6),
    }
    return render(request, 'store/tag_list.html', context)

from django.db.models import Q
from django.shortcuts import render
from .models import Product  

def search(request):
    query = request.GET.get('query')
    results = []

    if query:   
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    return render(request, 'store/search_results.html', {'query': query, 'results': results})
