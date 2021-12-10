from datetime import datetime
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import resolve

from .models import Analytic


# Is only allowed for admin user (or someone how got the "staff" status from another admin)
@staff_member_required()
def analytics_view(request):
    """
    View function for the analytics page.
    :param request: The web request.
    """
    register_visit(request, "Analyseseite")
    analytics = Analytic.objects.all()
    context = {
        "analytics": analytics,
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
