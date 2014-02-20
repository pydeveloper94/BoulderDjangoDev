from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(request=None, model=None, model_filters=None):
    """Paginates a group of objects based on the request parameters page and
    count, the model provided, and which models should be filtered.
    """
    if (request == None) or (model == None):
        raise Exception("You must pass in the request and model parameters.")
    # Correctly parse the query string and set default values if applicable
    page = request.GET.get('page', 1)
    count = request.GET.get('count')
    try:
        count = int(count)
    except:
        count = 10
    if (count > 100) or (count < 1):
        count = 10
    try:
        page = int(page)
    except:
        page = 1
    if page < 1:
        page = 1

    # Filter out the correct models
    if model_filters != None:
        models = model.objects.all().filter(**model_filters)
    else:
        models = model.objects.all()
    paginator = Paginator(models, count)

    # Finally, return the paginator object
    try:
        page =  paginator.page(page)
        return page
    except EmptyPage as e:
        return paginator.page(paginator.num_pages)
