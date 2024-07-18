"""Custom validators for the authentication app."""
import re

from django.conf import settings
from django.core.exceptions import ValidationError


class FileValidator:
    """Custom file validator class."""

    def __init__(self):
        self.max_size = settings.MAX_IMAGE_SIZE

    @staticmethod
    def validate_not_empty_file(value: object) -> object:
        """Validate if the filed is not empty."""
        if not value:
            raise ValidationError("Please upload a copy of CR Attachment.")

    @staticmethod
    def validate_image_file(value: object) -> object:
        """Validate the type of a file upload."""
        if value:
            if not value.name.lower().endswith(
                (".png", ".jpg", ".jpeg", ".pdf", "doc", "docx")
            ):
                raise ValidationError(
                    "The uploaded file must be a PNG , JPG or PDF file."
                )

    @staticmethod
    def validate_file_upload_size(value: object) -> object:
        """Validate the size of a file upload."""
        if value.size > settings.MAX_IMAGE_SIZE:
            raise ValidationError("File size must be no more than 5MB.")

    @staticmethod
    def arabic_to_english(numerals: str) -> str:
        arabic_english_map = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        return numerals.translate(arabic_english_map)

    def phone_number_validator(value):
        english_number = FileValidator.arabic_to_english(value)
        if not re.match(r'^0?[0-9]{9}$', english_number):
            raise ValidationError('Please enter a valid phone number with 9 digits.')
