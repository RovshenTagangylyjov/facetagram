import uuid
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def get_compressed_image_content(image_field_file: ContentFile, dimensions: list) -> ContentFile:
    img_io = BytesIO()
    img = Image.open(image_field_file)
    img.thumbnail(dimensions, Image.ANTIALIAS)
    new_name = f"{str(uuid.uuid4())}.{img.format}"
    img.save(img_io, format='png', quality=70, optimize=True)
    return ContentFile(img_io.getvalue(), new_name)
