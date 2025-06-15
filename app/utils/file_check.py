def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    ALLOWED_EXTENSIONS = {'.txt', '.epub', '.pdf'}

    # Find the last period in the filename
    idx = filename.rfind('.')

    # If no period found, it has no extension
    if idx == -1:
        return False

    # Extract the extension (including the period)
    file_extension = filename[idx:]

    # Check if it's in our allowed list
    return file_extension in ALLOWED_EXTENSIONS
