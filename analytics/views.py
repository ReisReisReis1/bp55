from datetime import datetime
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import resolve
from django.utils.datastructures import MultiValueDictKeyError

from .models import Analytic


# Is only allowed for admin user (or someone how got the "staff" status from another admin)
@staff_member_required()
def analytics_view(request):
    """
    View function for the analytics page.
    :param request: The web request.
    """
    register_visit(request, "Analyseseite")

    # check if there are url parameters for which month or year is requested,
    # otherwise set it to the current ones
    dt = datetime.now()
    try:
        wanted_year = request.GET["year"]
    except MultiValueDictKeyError:
        wanted_year = str(dt.year)
    try:
        wanted_month = request.GET["month"]
    except MultiValueDictKeyError:
        wanted_month = str(dt.month)

    analytics_raw = Analytic.objects.all().filter(year=wanted_year).filter(month=wanted_month)
    possible_years = [str(ps["year"]) for ps in Analytic.objects.values("year").order_by("year").distinct()]

    sorted_raw = {}

    base_url = "https://ruinsandbeyond.architektur.tu-darmstadt.de/"
    # for testing purposes:
    # base_url = "http://127.0.0.1:8000/"

    pages_raw = filter(lambda a: a.site_url not in ("search", "download", "details_page"), analytics_raw)
    buildings_raw = filter(lambda a: a.site_url == "details_page", analytics_raw)
    search_raw = filter(lambda a: a.site_url == "search", analytics_raw)
    downloads_raw = filter(lambda a: a.site_url == "download", analytics_raw)
    pages = sorted(pages_raw, key=lambda a: a.visits, reverse=True)
    for page in pages:
        page.site_url = base_url+page.site_url
    pages_count = sum([p.visits for p in pages])
    buildings = sorted(buildings_raw, key=lambda a: a.visits, reverse=True)
    for building in buildings:
        name, building_id = building.name.split(",")
        building.name = name+" (ID: "+building_id+")"
        # add id to site url, to get on correct detailspage
        building.site_url = base_url+building.site_url+"/"+building_id+"/"
    buildings_count = sum([b.visits for b in buildings])
    search_terms = sorted(search_raw, key=lambda a: a.visits, reverse=True)
    searches = sum([s.visits for s in search_terms])
    for st in search_terms:
        st.site_url = base_url+st.site_url+"/?search_request="+st.name
    downloads = sorted(downloads_raw, key=lambda a: a.visits, reverse=True)
    for d in downloads:
        d.name = d.name.split(",")[1]
        d.site_url = base_url+"materials_page/"+d.name
    dl_count = sum([dl.visits for dl in downloads])
    #re-describe month with month names
    md = {
            "1": "Januar",
            "2": "Februar",
            "3": "März",
            "4": "April",
            "5": "Mai",
            "6": "Juni",
            "7": "Juli",
            "8": "August",
            "9": "September",
            "10": "Oktober",
            "11": "November",
            "12": "Dezember",
          }
    wanted_month = md[wanted_month]

    context = {
        "year": wanted_year,
        "month": wanted_month,
        "possible_years": possible_years,
        "pages_count": pages_count,
        "pages": pages,
        "buildings_count": buildings_count,
        "buildings": buildings,
        "search_count": searches,
        "search_terms": search_terms,
        "download_count": dl_count,
        "zip_downloads": downloads,
    }
    return render(request, context=context, template_name="analytics.html")


def register_visit(request, name, alter_url=None):
    """
    Function for registering a visit to the analytics.
    It will update the database accordingly (add a visit to the current month/year to this url).
    :param request: request to extract the visited url from (for matching).
    :param name: a name tag for the visited url (for matching and pretty-print).
    :param alter_url: Give a url in string, not from a subpages' request (maybe useful for video
    clicks, ...). Will override the use of request, if it is set / not None.
    """
    dt = datetime.now()
    curr_month = dt.month
    curr_year = dt.year
    if alter_url is None:
        url = str(resolve(request.path_info).url_name)
    else:
        url = alter_url
    try:
        # try to find existing entry in the database
        entry = Analytic.objects.get(site_url=url, name=name, month=curr_month, year=curr_year)
        entry.visits += 1
        entry.save()
    except Analytic.DoesNotExist:
        # it is not there we have to add it
        new_entry = Analytic(site_url=url, name=name, month=curr_month, year=curr_year, visits=1)
        new_entry.save()
    except Analytic.MultipleObjectsReturned:
        # if there are multiple (which should not exists), collapse them.
        entries = Analytic.objects.filter(site_url=url, name=name, month=curr_month, year=curr_year)
        # keep the first one, and update it to all visits from the duplicates
        first = entries[0]
        visit_sum = first.visits
        for entry in entries:
            if entry == first:
                continue
            else:
                visit_sum += entry.visits
                entry.delete()
        first.visits = visit_sum
        first.save()
    return
