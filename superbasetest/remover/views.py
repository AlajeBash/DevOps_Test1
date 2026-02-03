from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import UploadedImage
from rembg import remove, new_session
from PIL import Image
import io
import os

# Global variable to hold the session
session = None

def get_session():
    global session
    if session is None:
        session = new_session("u2net")
    return session

def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # 1. Save Original Image
        original_file = request.FILES['image']
        obj = UploadedImage.objects.create(original_image=original_file)
        
        # 2. Read image and remove background
        # Using .open() and .read() makes it compatible with both local and S3 storage
        input_data = obj.original_image.open('rb').read()
        
        # rembg.remove does the AI magic here
        output_data = remove(input_data, session=get_session())
        
        # 3. Save the processed image back to the model
        processed_filename = f"bg_removed_{os.path.basename(obj.original_image.name)}"
        obj.processed_image.save(processed_filename, ContentFile(output_data))
        obj.save()
        
        return render(request, 'remover/index.html', {
            'obj': obj,
            'success': True
        })

    return render(request, 'remover/index.html')
