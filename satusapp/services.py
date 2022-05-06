from django.core.paginator import Paginator


def get_paginated_list(request, lst, number):
    paginator = Paginator(lst, number)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
