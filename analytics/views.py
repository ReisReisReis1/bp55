import csv
from datetime import datetime
from io import StringIO
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import resolve
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from .models import Analytic
from video_content.models import Video
from materials_page.models import Material


# Is only allowed for admin user (or someone how got the "staff" status from another admin)
@staff_member_required()
def analytics_view(request):
    """
    View function for the analytics page.
    :param request: The web request.
    """
    register_visit(request, "Analyseseite")

    base_url = "https://ruinsandbeyond.architektur.tu-darmstadt.de/"
    # for testing purposes:
    # base_url = "http://127.0.0.1:8000/"

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
    possible_years = [str(ps["year"]) for ps in
                      Analytic.objects.values("year").order_by("year").distinct()]

    sorted_raw = {}

    pages_raw = filter(lambda a: a.site_url not in ("search", "download", "details_page"),
                       analytics_raw)
    # filter out videos and pdf stuff:
    pages_raw = filter(lambda a: "media/videos" not in a.site_url, pages_raw)
    pages_raw = filter(lambda a: "media/material" not in a.site_url, pages_raw)
    buildings_raw = filter(lambda a: a.site_url == "details_page", analytics_raw)
    search_raw = filter(lambda a: a.site_url == "search", analytics_raw)
    downloads_raw = filter(lambda a: a.site_url == "download", analytics_raw)
    pdfs_raw = filter(lambda a: "media/material" in a.site_url, analytics_raw)
    videos_raw = filter(lambda a: "media/video" in a.site_url, analytics_raw)
    pages = sorted(pages_raw, key=lambda a: a.visits, reverse=True)
    for page in pages:
        page.site_url = base_url + page.site_url
    pages_count = sum([p.visits for p in pages])
    buildings = sorted(buildings_raw, key=lambda a: a.visits, reverse=True)
    for building in buildings:
        split = building.name.split(",")
        name, building_id = ",".join(split[:-1]), split[-1]
        building.name = name + " (ID: " + building_id + ")"
        # add id to site url, to get on correct detailspage
        building.site_url = base_url + building.site_url + "/" + building_id + "/"
    buildings_count = sum([b.visits for b in buildings])
    search_terms = sorted(search_raw, key=lambda a: a.visits, reverse=True)
    searches = sum([s.visits for s in search_terms])
    for st in search_terms:
        st.site_url = base_url + st.site_url + "/?search_request=" + st.name
    downloads = sorted(downloads_raw, key=lambda a: a.visits, reverse=True)
    for d in downloads:
        d.name = ",".join(d.name.split(",")[1:])
        d.site_url = base_url + "materials_page/" + d.name
    dl_count = sum([dl.visits for dl in downloads])
    pdfs = sorted(pdfs_raw, key=lambda a: a.visits, reverse=True)
    for p in pdfs:
        split = p.name.split(",")
        pdf_name, pdf_id = ",".join(split[:-1]), split[-1]
        p.name = pdf_name+" (ID: "+pdf_id+")"
        p.site_url = base_url + p.site_url
    pdf_count = sum([p.visits for p in pdfs])
    videos = sorted(videos_raw, key=lambda a: a.visits, reverse=True)
    for v in videos:
        split = v.name.split(",")
        vid_name, vid_id = ",".join(split[:-1]), split[-1]
        v.name = vid_name+" (ID: "+vid_id+")"
        v.site_url = base_url + v.site_url
    video_clicks = sum([v.visits for v in videos])
    # re-describe month with month names
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

    semester = ""
    if dt.month in [10, 11, 12, 1, 2, 3]:
        if dt.month in [10, 11, 12]:
            semester = "Wintersemester "+str(dt.year)+"/"+str(dt.year+1)
        else:
            semester = "Wintersemester " + str(dt.year-1) + "/" + str(dt.year)
    else:
        semester = "Sommersemester " + str(dt.year)

    context = {
        "year": wanted_year,
        "month": wanted_month,
        "year_curr": dt.year,
        "month_curr": md[str(dt.month)],
        "semester": semester,
        "possible_years": possible_years,
        "pages_count": pages_count,
        "pages": pages,
        "buildings_count": buildings_count,
        "buildings": buildings,
        "search_count": searches,
        "search_terms": search_terms,
        "download_count": dl_count,
        "zip_downloads": downloads,
        "pdf_count": pdf_count,
        "pdfs": pdfs,
        "video_count": video_clicks,
        "videos": videos,
    }
    return render(request, context=context, template_name="analytics.html")


@staff_member_required()
def analytics_download_view(request):
    """
    Download all analytics as .csv.
    :param request: The web request.
    """
    fields = ["URL", "Bezeichnung(,ID)", "Monat", "Jahr", "Anzahl Aufrufe"]
    all = Analytic.objects.all()
    rows = []
    for a in all:
        rows.append([a.site_url, a.name, str(a.month), str(a.year), str(a.visits)])
    dt = datetime.now()
    filename = "analytics-export-"+str(dt.day)+"-"+str(dt.month)+"-"+str(dt.year)+".csv"

    # open file in-memory
    sio = StringIO()

    # writing to csv file

    # creating a csv writer object
    csvwriter = csv.writer(sio, delimiter=';')
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(rows)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(sio.getvalue(), content_type="application/csv")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % filename
    sio.close()
    return resp




class LineChartJSONView(BaseLineChartView):
    """
    View for the chart.
    """

    sose = ["April", "Mai", "Juni", "Juli", "August", "September"]
    wise = ["Oktober", "November", "Dezember", "Januar", "Februar", "März"]

    def get_labels(self):
        """Return 6 labels for the x-axis."""
        dt = datetime.now()
        if dt.month in [4, 5, 6, 7, 8, 9]:
            res = []
            for m in self.sose:
                res.append(m+" "+str(dt.year))
            return res
        else:
            res = []
            if dt.month in [10, 11, 12]:
                for i in range(3):
                    res.append(self.wise[i]+" "+str(dt.year))
                for i in range(3, 6):
                    res.append(self.wise[i]+" "+str(dt.year+1))
            else:
                for i in range(3):
                    res.append(self.wise[i]+" "+str(dt.year-1))
                for i in range(3, 6):
                    res.append(self.wise[i]+" "+str(dt.year))
            return res

    def get_providers(self):
        """Return names of datasets."""
        return ["Alle erhobenen Zugriffe", "Material Zugriffe", "Gebäude Zugriffe", "Videoaufrufe", "Suchen"]

    def get_data(self):
        """Return datasets to plot."""
        all = Analytic.objects.all()
        buildings = all.filter(site_url="details_page")
        downloads = all.filter(site_url="download")
        pdfs = all.filter(site_url__contains="media/material")
        videos = all.filter(site_url__contains="media/video")
        searches = all.filter(site_url="search")
        data_all = []
        data_pdfs = []
        data_videos = []
        data_buildings = []
        data_searches = []
        dt = datetime.now()
        if dt.month not in [4, 5, 6, 7, 8, 9]:
            # is wise
            if dt.month in [10, 11, 12]:
                for i in range(10, 13):
                    data_all.append(sum(a.visits for a in all.filter(year=dt.year).filter(month=i)))
                    data_pdfs.append(sum(a.visits for a in pdfs.filter(year=dt.year).filter(month=i))+sum(
                        a.visits for a in downloads.filter(year=dt.year).filter(month=i)))
                    data_videos.append(sum(a.visits for a in videos.filter(year=dt.year).filter(month=i)))
                    data_buildings.append(sum(a.visits for a in buildings.filter(year=dt.year).filter(month=i)))
                    data_searches.append(sum(a.visits for a in searches.filter(year=dt.year).filter(month=i)))
                for i in range(1, 4):
                    data_all.append(sum(a.visits for a in all.filter(year=dt.year+1).filter(month=i)))
                    data_pdfs.append(sum(a.visits for a in pdfs.filter(year=dt.year+1).filter(month=i)) + sum(
                        a.visits for a in downloads.filter(year=dt.year+1).filter(month=i)))
                    data_videos.append(sum(a.visits for a in videos.filter(year=dt.year+1).filter(month=i)))
                    data_buildings.append(sum(a.visits for a in buildings.filter(year=dt.year+1).filter(month=i)))
                    data_searches.append(sum(a.visits for a in searches.filter(year=dt.year+1).filter(month=i)))
            else:
                for i in range(10, 13):
                    data_all.append(sum(a.visits for a in all.filter(year=dt.year-1).filter(month=i)))
                    data_pdfs.append(sum(a.visits for a in pdfs.filter(year=dt.year-1).filter(month=i)) + sum(
                        a.visits for a in downloads.filter(year=dt.year-1).filter(month=i)))
                    data_videos.append(sum(a.visits for a in videos.filter(year=dt.year-1).filter(month=i)))
                    data_buildings.append(sum(a.visits for a in buildings.filter(year=dt.year-1).filter(month=i)))
                    data_searches.append(sum(a.visits for a in searches.filter(year=dt.year-1).filter(month=i)))
                for i in range(1, 4):
                    data_all.append(sum(a.visits for a in all.filter(year=dt.year).filter(month=i)))
                    data_pdfs.append(sum(a.visits for a in pdfs.filter(year=dt.year).filter(month=i)) + sum(
                        a.visits for a in downloads.filter(year=dt.year).filter(month=i)))
                    data_videos.append(sum(a.visits for a in videos.filter(year=dt.year).filter(month=i)))
                    data_buildings.append(sum(a.visits for a in buildings.filter(year=dt.year).filter(month=i)))
                    data_searches.append(sum(a.visits for a in searches.filter(year=dt.year).filter(month=i)))
        else:
            # is sose
            for i in range(4, 10):
                data_all.append(sum(a.visits for a in Analytic.objects.filter(year=dt.year).filter(month=i)))
                data_pdfs.append(sum(a.visits for a in pdfs.filter(year=dt.year).filter(month=i)) + sum(
                    a.visits for a in downloads.filter(year=dt.year).filter(month=i)))
                data_videos.append(sum(a.visits for a in videos.filter(year=dt.year).filter(month=i)))
                data_buildings.append(sum(a.visits for a in buildings.filter(year=dt.year).filter(month=i)))
                data_searches.append(sum(a.visits for a in searches.filter(year=dt.year).filter(month=i)))
        return [data_all, data_pdfs, data_buildings, data_videos, data_searches]


line_chart = TemplateView.as_view()
line_chart_json = LineChartJSONView.as_view()


def add_visit(request, page, object_id):
    """
    Adds an endpoint to add visits for frontend-only stuff.
    This uses django's url layout, not url parameters to minimize chances of abuse for
    users and injections. This function will translate the url parts into the correct
    format for the register_visit and will add the visit. Also, it will validate the
    inputs for further minimization of abuse.
    Adds it for the current month. Will return either "OK" or "FAILED" on the page.
    :param request: The web request.
    :param page: The page that was visited (should either be 'video' or 'pdf').
    :param object_id: The id of the tracked object (video or material pdf).
    """
    # the add will be posted by javascript, so check for it
    if request.method != "POST":
        raise PermissionDenied
    elif page not in ["video", "pdf"]:
        raise PermissionDenied
    else:
        if page == "video":
            # get media url for video
            video = Video.objects.get(id=object_id)
            site = video.video.url[1:]
            # resolve name
            name = video.title+","+str(object_id)
            register_visit(request, name, alter_url=site)
        elif page == "pdf":
            # get media url for material pdf
            file = Material.objects.get(id=object_id)
            site = file.file.url[1:]
            # resolve name
            name = file.name+","+str(object_id)
            register_visit(request, name, alter_url=site)
        else:
            raise PermissionDenied
    return render(request, template_name="add_visit.html")


@staff_member_required()
def delete_old(request):
    """
    Upon visiting this url, all older (or to be exact other) month of analytics data will be deleted.
    :param request: The web request.
    """
    dt = datetime.now()
    curr_month = dt.month
    curr_year = dt.year
    Analytic.objects.exclude(year=curr_year, month=curr_month).delete()
    return redirect("/analytics/")


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
