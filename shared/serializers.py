import base64
import tempfile
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """
    Custom Image field to handle base64 encoded image for POST requests.
    """

    def to_internal_value(self, data):
        """
        Convert base64 string to Image file during POST request.
        """
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            try:
                # Decode the base64 string
                image_data = base64.b64decode(imgstr)
                # Create a temporary file name or use a default
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(image_data)
                temp_file.close()  # Close the file after writing

                # Open the file with Django's ContentFile
                with open(temp_file.name, 'rb') as f:
                    image_file = ContentFile(f.read(), name='uploaded_image.png')  # Provide a filename

                # Return the in-memory file object
                return super().to_internal_value(image_file)
            except Exception as e:
                raise serializers.ValidationError(f"Invalid base64 image: {str(e)}")
        else:
            return super().to_internal_value(data)

    def to_representation(self, value):
        """
        Convert to base64 for POST request, and URL for GET request
        """
        # Check if it's a GET request or POST request
        request = self.context.get('request')

        if request and request.method == 'GET':
            if value:
                # Return the URL of the image
                return request.build_absolute_uri(value.url)
            return None
        else:
            # For POST requests, return the base64 encoded string
            if value:
                with BytesIO() as buffer:
                    img = Image.open(value)
                    img.save(buffer, format='PNG')
                    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    return img_str
            return None
