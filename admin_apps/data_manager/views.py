# Create your views here.
from django import http
import json
from django import forms as forms
from django.shortcuts import render_to_response
from django.http import HttpResponse

#PR: storage
import os
import hashlib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
######

FILEFOLDER = 'FileFolders'

from admin_apps.data_manager.models import FileFolder

class SimpleFileForm(forms.Form):
    file = forms.Field(widget=forms.FileInput, required=False)


def add_filefolder(file_list, subfolder=""):
    file_list.sort(key=str) #PR: sort list by file names
    rel_path_folder = os.path.join(FILEFOLDER, subfolder)
    new_file_folder = FileFolder()
    new_file_folder.save() #PR; save to generate uuid
    try:
        folder_sha1 = hashlib.sha1()
        for form_file in file_list:#request.FILES.getlist('form_files'):
            path = default_storage.save(
                os.path.join(
                    rel_path_folder,
                    new_file_folder.uuid,
                    form_file.name),
                ContentFile(form_file.read()))
            abs_path = os.path.join(settings.MEDIA_ROOT, path)
            print abs_path
            f = open(abs_path, 'rb')
            try:
                file_sha1 = hashlib.sha1(f.read())
                folder_sha1.update(file_sha1.hexdigest())
            finally:
                f.close()
            print file_sha1.hexdigest()
        print folder_sha1.hexdigest()
        new_file_folder.checksum = folder_sha1.hexdigest()
        new_file_folder.save()
        return new_file_folder
    except: #TODO: How to treat this exception?
        new_file_folder.delete()
        return None


def directupload(request):
    """
    Saves the file directly from the request object.
    Disclaimer:  This is code is just an example, and should
    not be used on a real website.  It does not validate
    file uploaded:  it could be used to execute an
    arbitrary script on the server.
    """

    template = 'fileupload.html'

    if request.method == 'POST':
        #print request.FILES
        #if form.is_valid():
        add_filefolder(request.FILES.getlist('form_files'))
        # Redirect to the document list after POST
        return HttpResponse("OK") #Redirect(reverse('data_manager.views.directupload'))
        """
        if 'file' in request.FILES:
            file = request.FILES['file']

            # Other data on the request.FILES dictionary:
            #   filesize = len(file['content'])
            #   filetype = file['content-type']

            filename = file['filename']

            fd = open('%s/%s' % (settings['MEDIA_ROOT'], filename), 'wb')
            fd.write(file['content'])
            fd.close()

            return http.HttpResponseRedirect(' upload_success.html')
        """
    else:
        # display the form
        form = SimpleFileForm()
        return render_to_response(template)

def upload_imagestacks(request):
    pass