ALLOWED_EXTENSIONS = frozenset({'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'txt', 'mp4', 'mp3', 'zip'})


def is_allowed_extension(filename):
    if not filename:
        return False
    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return extension in ALLOWED_EXTENSIONS
