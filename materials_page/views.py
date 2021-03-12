"""
Configurations of the Website subpages from the App: materials_page
"""
# pylint: disable = import-error, relative-beyond-top-level
from start.views import login_required
from .models import Material

from zipfile import ZipFile
from io import StringIO
from io import BytesIO
import zipfile
import os
from django.shortcuts import render
from django.http import HttpResponse
from impressum.views import get_course_link
from .models import Material


def get_categories_and_corresponding_files():
    """
    :return: the categories and corresponding material in a dictionary
    """
    result = dict()
    # Add all the existing categories and material-files in one dictionary
    for material_entry in Material.objects.all():
        # If the category is not already in the dictionary, add category and file as first element
        if material_entry.get_category not in result:
            result[material_entry.get_category] = [material_entry]
        # If the category is already in the dictionary, add file to this category
        else:
            result[material_entry.get_category] = result[material_entry.get_category] + [material_entry]
    return result


# Hier einkommentieren für SSO:
#@login_required
def get_categories_and_corresponding_zip_files(request):
    """
    :return: the categories and HttpsResponse for the corresponding zip files in a dictionary
    """

    material_dict = get_categories_and_corresponding_files()
            # the zip compressor
            zf = zipfile.ZipFile(s, "w")

            # Add all file sin the list to the zipfile
            for fpath in filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                # Add file, at correct path
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            # Add HttpResponse to download zipfile to the dictionary at the place of the category
            material_dict[category_entry] = resp
    return material_dict


# Hier einkommentieren für SSO:
#@login_required
def material(request):

    """
    Subpage to show the characteristics of a building
    :param request: url request to get materials_page
    :param category: name of the category to return only elements of this category
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """

    context = {
        'Materials': get_categories_and_corresponding_files(),

        'Zip_Files': get_categories_and_corresponding_zip_files(category),

        'Kurs_Link': get_course_link()
    }
    return render(request, "material.html", context)
