"""
uv run code/multipart_upload_client.py
"""

from pathlib import Path

FILE_PATH = Path("code/fixtures/sample-document.pdf")
PART_SIZE = 5 * 1024 * 1024  # 5 MiB


def inspect_file(file_path: Path):
    file_size = file_path.stat().st_size
    number_of_parts = (file_size + PART_SIZE - 1) // PART_SIZE

    print(f"File          : {file_path.name}")
    print(f"File size     : {file_size:,} bytes")
    print(f"Part size     : {PART_SIZE:,} bytes")
    print(f"Number parts  : {number_of_parts}")

    return file_size, number_of_parts


def main():
    inspect_file(FILE_PATH)


if __name__ == "__main__":
    main()
