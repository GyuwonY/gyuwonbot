class FileUploadError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class UnsupportedFileTypeError(FileUploadError):
    def __init__(self, filename: str):
        super().__init__(f"Unsupported file type: {filename}")


class CSVProcessingError(FileUploadError):
    def __init__(self, filename: str, original_exception: Exception):
        detail = f"Error processing CSV file {filename}: {original_exception}"
        super().__init__(detail)


class MDProcessingError(FileUploadError):
    def __init__(self, filename: str, original_exception: Exception):
        detail = f"Error processing Markdown file {filename}: {original_exception}"
        super().__init__(detail)
