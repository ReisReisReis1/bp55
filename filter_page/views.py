"""
Configurations of the different viewable functions and subpages from the App: home
"""
from django.db.models import Q
from django.shortcuts import render
from details_page.models import Building, Era
from timeline.views import get_thumbnails_for_buildings


def my_filter(lst, key, value):
    """
    This will execute filtering on a given list, while given key as string.
    This is meant for the view method below, i want to use filter(key=value) is the call.
    But key is a name of a parameter, i only have it as python string.
    To solve this, this method was created. It just use the string case, and
    execute the same filter.
    :param lst: the list to filter on.
    :param key: the key to filter on, as string.
    :param value: the value to filter by.
    :return: the filtered lst, filtered by the value with the key.
    """
    if key == "era":
        return lst.filter(era__name=value)
    elif key == "country":
        return lst.filter(country=value)
    elif key == "region":
        return lst.filter(region=value)
    elif key == "city":
        return lst.filter(city=value)
    elif key == "architect":
        return lst.filter(architect=value)
    elif key == "builder":
        return lst.filter(builder=value)
    elif key == "column_order":
        return lst.filter(column_order=value)
    elif key == "design":
        return lst.filter(design=value)
    else:
        return lst


def display_building_filter(request):
    """
    Subpage "Gebäudefilter" with context
    :param request: url request to get subpage /filter
    :return: rendering the subpage based on filter.html with context
    context: Variable to filter all buildings with the criteria got from the request
    """

    # We can filter by this options:
    # era, country, region, city, architect, builders, column_orders, designs
    keys = ["era", "country", "region", "city", "architect", "builder", "column_order", "design"]
    q = request.GET
    # Set all, to return all.
    # This will take care of returning all Buildings, if no filter is set.
    result = Building.objects.all()

    # If there is something set, it will start filtering here:
    for key in keys:
        if key in q:
            # If here the key is in it, it will be filtered by.
            querys = q.getlist(key)
            if len(querys) > 1:
                # Here it is an list with more than one elements.
                # Therefore we will not update data types.
                result_for_lst = None
                for query in querys:
                    # There are more then one of this filter type (key): Use of OR on the results.
                    # OR means we keep all filterings, just discard duplications.
                    # Therefore we added up everything here, just need to check, if there are duplications
                    if result_for_lst is None:
                        result_for_lst = my_filter(result, key, query)
                    else:
                        # This will add querysets to each other:
                        # (Similar to SQL UNION Statment)
                        # result_for_lst = result_for_lst.union(my_filter(result, key, query), all=False)
                        result_for_lst = result_for_lst | my_filter(result, key, query)
                # Set it to the result. We had to work on a temporary var, otherwise
                # it would be impossible to use an OR logic (for AND it will be easier).
                result = result_for_lst
            elif len(querys) == 1 and querys[0] != "":
                # Here there is just one filter of its type.
                # Therefore we update datatype to string.
                query = querys[0]
                result = my_filter(result, key, query)
            else:
                # If length == 0: just pass
                pass
            # Different Key filters, will use AND on the results.
            # Will will archive this by just filtering on.
            # If the object meets all filters, it will be in the result.
        else:
            pass
            # Here we must take all of the objects in the list.
            # Theoretically we add everything here and do AND.
            # But this is unnecessary, because, we started with all()

    result = get_thumbnails_for_buildings(result)

    filter_names = ('Epoche', 'Land', 'Region', 'Stadt', 'Architekt', 'Erbauer', 'Säulenordnung', 'Design')
    buildings = Building.objects.all()
    eras = Era.objects.all().only('name')
    countries = buildings.only('country')
    regions = buildings.only('region')
    cities = buildings.only('city')
    architects = buildings.only('architect')
    builders = buildings.only('builder')
    column_orders = buildings.only('column_order')
    designs = buildings.only('design')
    context = {
        'Cities': cities,
        'Regions': regions,
        'Countries': countries,
        'Eras': eras,
        'Architects': architects,
        'Builders': builders,
        'Designs': designs,
        'Column_Orders': column_orders,
        'Filter_Result': result,
        'Filter_Names': filter_names,
    }

    return render(request, 'filter.html', context)


