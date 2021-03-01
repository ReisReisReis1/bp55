"""
Configurations of the Website subpages from the App: materials_page
"""


from django.shortcuts import render
# pylint: disable = import-error, relative-beyond-top-level
from .models import Material
from zipfile import ZipFile
from io import StringIO
from io import BytesIO
import zipfile
import os
from django.http import HttpResponse


def get_categories_and_corresponding_files():
    result = dict()
    for material_entry in Material.objects.all():
        if material_entry.category not in result:
            result[material_entry.category] = [material_entry]
        else:
            result[material_entry.category] = result[material_entry.category] + [material_entry]
    return result


def get_categories_and_corresponding_zip_files():
    """
            # Folder name in ZIP archive which contains the above files
            path = 'C:/Users/Laura Buhleier/Documents/GitHub/media/'
            zip_subdir = 'zipfiles'
            print('zip_supdir ' + zip_subdir)
            zip_filename = "%s.zip" % zip_subdir
            print('zip_filename ' + zip_filename)

            # Open StringIO to grab in-memory ZIP contents
            s = BytesIO()

            # the zip compressor
            zf = zipfile.ZipFile(s, "w")

            for fpath in filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                # Add file, at correct path
                print('zip_path ' + zip_path)
                print('fpath ' + fpath)
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

            return resp
            """
    material_dict = get_categories_and_corresponding_files()
    for category_entry in material_dict:
        # Files (local path) to put in the .zip
        filenames = []
        for material_entry in material_dict[category_entry]:
            filenames = filenames + [material_entry.file.path]

            # Folder name in ZIP archive which contains the above files
            path = 'C:/Users/Laura Buhleier/Documents/GitHub/media/'
            zip_subdir = 'zipfiles'
            zip_filename = "%s.zip" % zip_subdir

            # Open StringIO to grab in-memory ZIP contents
            s = BytesIO()

            # the zip compressor
            zf = zipfile.ZipFile(s, "w")

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
            material_dict[category_entry] = resp
    return material_dict


def material(request):
    """
    Subpage to show the characteristics of a building
    :param request: url request to get materials_page
    :return: rendering the subpage based on material.html
    with a context variable to get the characteristics
    """

    context = {
        'Materials': get_categories_and_corresponding_files(),
        'Zip_Files': get_categories_and_corresponding_zip_files(),
    }
    return render(request, "material.html", context)
