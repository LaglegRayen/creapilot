import os

def log_message(message):
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def handle_error(error):
    """Handles errors by logging them."""
    log_message(f"[ERROR] {error}")

def cleanup_temp_files(file_paths):
    """Deletes temporary files after processing."""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            log_message(f"Deleted temporary file: {file_path}")
        except Exception as e:
            handle_error(f"Failed to delete {file_path}: {e}")