"""
Configurations of the different viewable functions and subpages from the App: home
"""
# pylint: disable = no-name-in-module, import-error
import re
from django.shortcuts import render
from details_page.models import Building, Era
from start.views import login_required
from impressum.views import get_course_link
from announcements.views import get_announcements
from analytics.views import register_visit


def splitting(lst):
    """
    Splits the strings in the list at ; and ,
    """
    return_lst = []
    for string1 in lst:
        return_lst.extend(re.split(' , | ,|, |,| ; |; | ;|;| / |/ | /|/', string1))
    # Getting back all Elements that are not equal(__ne__) to '' (empty string)
    # https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
    return list(filter(''.__ne__, return_lst))


def one_dict_set_to_string_list(dictqs):
    """
    This will refactor the dict list queryset to a string list, with the same contents.
    :param dictqs: QuerySet with only a one parameter (from .values("<param-name>"))
    :return: this values from the inner dicts as a string list
    """
    str_lst = []
    for element in dictqs:
        for value in element.values():
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


# Hier einkommentieren für SSO:
#@login_required
def display_building_filter(request):
    # pylint: disable=too-many-locals
    """
    Subpage "Gebäudefilter" with context
    :param request: url request to get subpage /filter
    :return: rendering the subpage based on filter.html with context
    context: Variable to filter all buildings with the criteria got from the request
    """
    register_visit(request, "Filterseite")

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
                # Here it is an list with more than one element.
                # Therefore, we will not update data types.
                result_for_lst = None
                for query in querys:
                    # There are more than one of this filter type (key): Use of OR on the results.
                    # OR means we keep all filtering attributes, just discard duplications.
                    # Therefore, we added up everything here, just need to check,
                    # if there are duplications
                    if result_for_lst is None:
                        result_for_lst = my_filter(result, key, query)
                    else:
                        # This will add querysets to each other:
                        # (Similar to SQL UNION Statement)
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
    result = [(res, res.get_thumbnail()) for res in result]

    filter_names = ['Stadt', 'Region', 'Land', 'Epoche', 'Architekt', 'Bauherr', 'Bauform',
                    'Säulenordnung', 'Material', 'Gattung/Funktion']
    # pylint: disable = no-member
    buildings = Building.objects.all()
    # pylint: disable = no-member

    eras = Era.objects.all().exclude(name=None).values('name').distinct()
    eras = delete_duplicates(splitting(one_dict_set_to_string_list(eras)))
    eras = sorted(eras, key=lambda x: x.lower())

    countries = buildings.only('country').exclude(country=None).values('country').distinct()
    countries = delete_duplicates(splitting(one_dict_set_to_string_list(countries)))
    countries = sorted(countries, key=lambda x: x.lower())

    regions = buildings.only('region').exclude(region=None).values('region').distinct()
    regions = delete_duplicates(splitting(one_dict_set_to_string_list(regions)))
    regions = sorted(regions, key=lambda x: x.lower())

    cities = buildings.only('city').exclude(city=None).values('city').distinct()
    cities = delete_duplicates(splitting(one_dict_set_to_string_list(cities)))
    cities = sorted(cities, key=lambda x: x.lower())

    architects = buildings.only('architect').exclude(architect=None).values('architect').distinct()
    architects = delete_duplicates(splitting(one_dict_set_to_string_list(architects)))
    architects = sorted(architects, key=lambda x: x.lower())

    builders = buildings.only('builder').exclude(builder=None).values('builder').distinct()
    builders = delete_duplicates(splitting(one_dict_set_to_string_list(builders)))
    builders = sorted(builders, key=lambda x: x.lower())

    column_orders = buildings.only('column_order').exclude(column_order=None).values('column_order').distinct()
    column_orders = delete_duplicates(splitting(one_dict_set_to_string_list(column_orders)))
    column_orders = sorted(column_orders, key=lambda x: x.lower())

    designs = buildings.only('design').exclude(design=None).values('design').distinct()
    designs = delete_duplicates(splitting(one_dict_set_to_string_list(designs)))
    designs = sorted(designs, key=lambda x: x.lower())

    material = buildings.only('material').exclude(material=None).values('material').distinct()
    material = delete_duplicates(splitting(one_dict_set_to_string_list(material)))
    material = sorted(material, key=lambda x: x.lower())

    function = buildings.only('function').exclude(function=None).values('function').distinct()
    function = delete_duplicates(splitting(one_dict_set_to_string_list(function)))
    function = sorted(function, key=lambda x: x.lower())

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
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }

    return render(request, 'filter.html', context)
