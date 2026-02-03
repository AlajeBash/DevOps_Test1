from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import UploadedImage
from rembg import remove
from PIL import Image
import io
import os

def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # 1. Save Original Image
        original_file = request.FILES['image']
        obj = UploadedImage.objects.create(original_image=original_file)
        
        # 2. Get the path to the original image
        input_path = obj.original_image.path
        
        # 3. Read image and remove background
        with open(input_path, 'rb') as i:
            input_data = i.read()
            # rembg.remove does the AI magic here
            output_data = remove(input_data)
        
        # 4. Save the processed image back to the model
        # We use ContentFile to save the bytes from memory directly into the ImageField
        processed_filename = f"bg_removed_{os.path.basename(input_path)}"
        obj.processed_image.save(processed_filename, ContentFile(output_data))
        obj.save()
        
        return render(request, 'remover/index.html', {
            'obj': obj,
            'success': True
        })

    return render(request, 'remover/index.html')
