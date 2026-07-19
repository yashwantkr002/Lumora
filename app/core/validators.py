from django.core.exceptions import ValidationError


def validate_image_size(file):
    max_size = 10 * 1024 * 1024  # 10MB

    if file.size > max_size:
        raise ValidationError(
            "Image size cannot exceed 10 MB."
        )


def validate_video_size(file):
    max_size = 100 * 1024 * 1024  # 100MB

    if file.size > max_size:
        raise ValidationError(
            "Video size cannot exceed 100 MB."
        )


def validate_avatar(file):
    allowed = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if file.content_type not in allowed:
        raise ValidationError(
            "Only JPG, PNG and WEBP images are allowed."
        )

    validate_image_size(file)


def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10MB

    if file.size > max_size:
        raise ValidationError(
            "File size cannot exceed 10 MB."
        )
    
def validate_cover(file):
    allowed = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if file.content_type not in allowed:
        raise ValidationError(
            "Only JPG, PNG and WEBP images are allowed."
        )

    validate_image_size(file)