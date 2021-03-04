"""
Configurations of the different viewable functions and subpages from the App: home
"""
import re
from django.shortcuts import render
from details_page.models import Building, Era
from timeline.views import get_thumbnails_for_buildings
from impressum.views import get_course_link


def splitting(lst):
    """
    Splits the strings in the list at ; and ,
    """
    return_lst = []
    for s in lst:
        return_lst.extend(re.split(', | ; |;|,', s))
    # Getting back all Elements that are not equal(__ne__) to ''
    # https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
    return list(filter(''.__ne__, return_lst))


def one_dict_set_to_string_list(dictqs):
    """
    This will refactor the dict list queryset to a string list, with the same contents.
    :param dictqs: QuerySet with only a one parameter (from .values("<param-name>"))
    :return: this values from the inner dicts as a string list
    """
    str_lst = []
    for dict in dictqs:
        for value in dict.values():
            str_lst.append(value)
    return str_lst


def delete_duplicates(lst):
    """
    This will - wait for it - delete duplicates from the given list.
    Meant for deleting the duplicates from the QuerySets, therefore it fetches the .id fields.
    :param lst: the given list
    :return: the list without duplicates
    """
    result = []
    for entry in lst:
        if entry not in result:
            result.append(entry)
    return result


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
    # Have to do this workaround, cause pylint only allows one return at the end
    result = lst
    if key == "era":
        result = lst.filter(era__name=value)
    elif key == "country":
        result = lst.filter(country=value)
    elif key == "region":
        result = lst.filter(region__icontains=value)
    elif key == "city":
        result = lst.filter(city__icontains=value)
    elif key == "architect":
        result = lst.filter(architect__icontains=value)
    elif key == "builder":
        result = lst.filter(builder__icontains=value)
    elif key == "column_order":
        result = lst.filter(column_order__icontains=value)
    elif key == "design":
        result = lst.filter(design__icontains=value)
    elif key == "material":
        result = lst.filter(material__icontains=value)
    elif key == "function":
        result = lst.filter(function__icontains=value)
    else:
        result = lst
    return result


def display_building_filter(request):
    """
    Subpage "Gebäudefilter" with context
    :param request: url request to get subpage /filter
    :return: rendering the subpage based on filter.html with context
    context: Variable to filter all buildings with the criteria got from the request
    """

    # We can filter by this options:
    # era, country, region, city, architect, builders, column_orders, designs, material, function
    keys = ["era", "country", "region", "city", "architect", "builder", "column_order", "design",
            "material", "function"]
    urls_parameters = request.GET
    # Set all, to return all.
    # This will take care of returning all Buildings, if no filter is set.
    # pylint: disable = no-member
    result = Building.objects.all()

    # If there is something set, it will start filtering here:
    for key in keys:
        if key in urls_parameters:
            # If here the key is in it, it will be filtered by.
            querys = urls_parameters.getlist(key)
            if len(querys) > 1:
                # Here it is an list with more than one elements.
                # Therefore we will not update data types.
                result_for_lst = None
                for query in querys:
                    # There are more then one of this filter type (key): Use of OR on the results.
                    # OR means we keep all filterings, just discard duplications.
                    # Therefore we added up everything here, just need to check,
                    # if there are duplications
                    if result_for_lst is None:
                        result_for_lst = my_filter(result, key, query)
                    else:
                        # This will add querysets to each other:
                        # (Similar to SQL UNION Statment)
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

    # order results alphabetically
    result = result.order_by("name")
    # Append Thumbnails
    result = get_thumbnails_for_buildings(result)

    filter_names = ['Stadt', 'Region', 'Land', 'Epoche', 'Architekt', 'Bauherr', 'Bauform',
                    'Säulenordnung', 'Material', 'Funktion']
    # pylint: disable = no-member
    buildings = Building.objects.all()
    # pylint: disable = no-member
    eras = Era.objects.all().exclude(name=None).order_by("name").values('name')
    # Now we just need to delete all duplicates. We could use .distinct() for that,
    # but this only works on postgres Databases
    # (what is painful cause we use sqlite for development)
    # so we will implement duplication deletion in python here for this matter.
    # But later (if no one uses sqlite anymore)
    # it would be better and more efficient to set .distinct() for that.
    eras = delete_duplicates(splitting(one_dict_set_to_string_list(eras)))

    countries = buildings.only('country').exclude(country=None).order_by("country")\
        .values('country')
    countries = delete_duplicates(splitting(one_dict_set_to_string_list(countries)))

    regions = buildings.only('region').exclude(region=None).order_by("region").values('region')
    regions = delete_duplicates(splitting(one_dict_set_to_string_list(regions)))

    cities = buildings.only('city').exclude(city=None).order_by("city").values('city')
    cities = delete_duplicates(splitting(one_dict_set_to_string_list(cities)))

    architects = buildings.only('architect').exclude(architect=None).order_by("architect")\
        .values('architect')
    architects = delete_duplicates(splitting(one_dict_set_to_string_list(architects)))

    builders = buildings.only('builder').exclude(builder=None).order_by("builder").values('builder')
    builders = delete_duplicates(splitting(one_dict_set_to_string_list(builders)))

    column_orders = buildings.only('column_order').exclude(column_order=None)\
        .order_by("column_order").values('column_order')
    column_orders = delete_duplicates(splitting(one_dict_set_to_string_list(column_orders)))

    designs = buildings.only('design').exclude(design=None).order_by("design").values('design')
    designs = delete_duplicates(splitting(one_dict_set_to_string_list(designs)))

    material = buildings.only('material').exclude(material=None).order_by("material") \
        .values('material')
    material = delete_duplicates(splitting(one_dict_set_to_string_list(material)))

    function = buildings.only('function').exclude(function=None).order_by("function") \
        .values('function')
    function = delete_duplicates(splitting(one_dict_set_to_string_list(function)))

    context = {
        'Cities': cities,
        'Regions': regions,
        'Countries': countries,
        'Eras': eras,
        'Architects': architects,
        'Builders': builders,
        'Designs': designs,
        'Column_Orders': column_orders,
        'Materials': material,
        'Functions': function,
        'Filter_Result': result,
        'Filter_Names': filter_names,
        'Active_Filter': dict(urls_parameters),
        'Kurs_Link': get_course_link()
    }

    return render(request, 'filter.html', context)
