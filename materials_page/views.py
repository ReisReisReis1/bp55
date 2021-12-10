"""
Configurations of the Website subpages from the App: materials_page
"""
# pylint: disable = all
from start.views import login_required
from .models import Material

from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Material
from zipfile import ZipFile
from io import StringIO
from io import BytesIO
import zipfile
import os
from django.http import HttpResponse
from impressum.views import get_course_link
from announcements.views import get_announcements
from analytics.views import register_visit


def get_categories_and_corresponding_files():
    """
    :return: the categories and corresponding material in a dictionary
    """
    result = dict()
    # Add all the existing categories and material-files in one dictionary
    for material_entry in Material.objects.all():
        # If the category is not already in the dictionary, add category and file as first element
        if material_entry.get_category() not in result:
            result[material_entry.get_category()] = [material_entry]
        # If the category is already in the dictionary, add file to this category
        else:
            result[material_entry.get_category()] = result[material_entry.get_category()] + [
                material_entry]
    return result


# Hier einkommentieren für SSO:
#@login_required
def get_categories_and_corresponding_zip_files(request, category):
    #
    """
    :return: the categories and HttpsResponse for the corresponding zip files in a dictionary
    """
    register_visit(request, "Download Material .zip für Kategorie "+category)
    material_dict = get_categories_and_corresponding_files()
    # Get all material files of one category in a single list
    # Files (local path) to put in the .zip
    filenames = []
    resp = None
    for material_entry in material_dict[category]:
        filenames = filenames + [material_entry.file.path]

        # Folder name in ZIP archive which contains the above files
        zip_subdir = category
        zip_filename = "%s.zip" % zip_subdir

        # Open BytesIO to grab in-memory ZIP contents
        sio = BytesIO()

        # the zip compressor
        zf1 = zipfile.ZipFile(sio, "w")

        # Add all file sin the list to the zipfile
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            # Add file, at correct path
            zf1.write(fpath, zip_path)

        # Must close zip for all contents to be written
        zf1.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(sio.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp


#@login_required
def material(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get materials_page
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """
    register_visit(request, "Materialseite")
    # this code ist for adding colors to the materials
    # for visual difference, both colors will take turns
    colors = ["2F4B33", "B43B44"]
    materials = get_categories_and_corresponding_files()
    materials_with_colors = []
    i = 0
    for category in materials.keys():
        color = None
        nextcolor = None
        if i % 2 == 0:
            color = colors[0]
            nextcolor = colors[1]
        else:
            color = colors[1]
            nextcolor = colors[0]
        materials_with_colors.append([category, materials[category], color, nextcolor])
        i += 1

    context = {
        'Materials': materials_with_colors,
        'Kurs_Link': get_course_link(),
        'announcements': get_announcements(),
    }
    return render(request, "material.html", context)
