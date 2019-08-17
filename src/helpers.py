"""Miscellaneous helper functions for the app."""


def file_size_format(size, suffix="B"):
    """Given a file size, return a string with its standard compressed form."""
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if size < 1024:
            break
        size /= 1024
    else:
        unit = "Yi"

    return f"{size:.1f} {unit}{suffix}"
