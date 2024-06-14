from django.shortcuts import get_object_or_404, render

from .models import Item, ItemTag
from .paginator import paginator
from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)


def store(request):
    items = Item.objects.filter(is_available=True)
    context = {
        "page_obj": paginator(request, items, 9),
        "range": [*range(1)],
    }

    return render(request, "store/main_page.html", context)


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {
        "item": item,
    }
    return render(request, "store/item_details.html", context)


def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])
    context = {
        "tag": tag,
        "page_obj": paginator(request, items, 3),
    }
    return render(request, "store/tag_details.html", context)


def tag_list(request):
    tags = ItemTag.objects.all()
    context = {
        "page_obj": paginator(request, tags, 6),
    }
    return render(request, "store/tag_list.html", context)


from django.db.models import Q
from django.shortcuts import render
from .models import Item


def search(request):
    query = request.GET.get("query")
    results = []
    print(f"{query=} {type(query)=}")
    print(f"{Item.objects.all()=}")

    if query:
        # results = Item.objects.filter(
        #     Q(title__contains=query) | Q(description__contains=query)
        # )
        query_lower = query.lower()
        results = Item.objects.filter(
            Q(title__lower__icontains=query_lower)
            | Q(description__lower__icontains=query_lower)
        )
        print(f"{results=}")

    return render(
        request, "store/search_results.html", {"query": query, "results": results}
    )
