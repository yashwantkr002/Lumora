from django.core.exceptions import ValidationError


def validate_avatar(file):
    if not file:
        return
    if getattr(file, "size", 0) > 5 * 1024 * 1024:
        raise ValidationError("Avatar image must be 5MB or less.")


def validate_cover(file):
    if not file:
        return
    if getattr(file, "size", 0) > 10 * 1024 * 1024:
        raise ValidationError("Cover image must be 10MB or less.")


def validate_image_size(file):
    if not file:
        return
    if getattr(file, "size", 0) > 10 * 1024 * 1024:
        raise ValidationError("Image size must be 10MB or less.")


def validate_file_size(file, max_size):
    if not file:
        return
    if getattr(file, "size", 0) > max_size:
        raise ValidationError(f"File size must be {max_size} bytes or less.")


def validate_video_size(file):
    if not file:
        return
    if getattr(file, "size", 0) > 200 * 1024 * 1024:
        raise ValidationError("Video size must be 200MB or less.")
