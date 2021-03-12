"""
Configurations of the Website subpages from the App: materials_page
"""


from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from start.views import login_required
from .models import Material
from zipfile import ZipFile
from io import StringIO
from io import BytesIO
import zipfile
import os
from django.http import HttpResponse
from impressum.views import get_course_link


def get_categories_and_corresponding_files():
    """
    :return: the categories and corresponding material in a dictionary
    """
    result = dict()
    # Add all the existing categories and material-files in one dictionary
    for material_entry in Material.objects.all():
        # If the category is not already in the dictionary, add category and file as first element
        if material_entry.category not in result:
            result[material_entry.category] = [material_entry]
        # If the category is already in the dictionary, add file to this category
        else:
            result[material_entry.category] = result[material_entry.category] + [material_entry]
    return result


# Hier einkommentieren für SSO:
#@login_required
def get_categories_and_corresponding_zip_files(request):
    """
    :return: the categories and HttpsResponse for the corresponding zip files in a dictionary
    """

    material_dict = get_categories_and_corresponding_files()
    # zip the content of each category
    for category_entry in material_dict:
        # Get all material files of one category in a single list
        # Files (local path) to put in the .zip
        filenames = []
        for material_entry in material_dict[category_entry]:
            filenames = filenames + [material_entry.file.path]

            # Folder name in ZIP archive which contains the above files
            zip_subdir = 'zipfiles'
            zip_filename = "%s.zip" % zip_subdir

            # Open BytesIO to grab in-memory ZIP contents
            s = BytesIO()

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
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """

    context = {
        'Materials': get_categories_and_corresponding_files(),
        'Zip_Files': get_categories_and_corresponding_zip_files(request),
        'Kurs_Link': get_course_link()
    }
    return render(request, "material.html", context)

