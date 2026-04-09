from local_lib.path import Path


def using_path_lib():
    test_folder = Path("test_folder")
    test_folder.mkdir_p()
    test_file = test_folder / "test_file.txt"
    test_file.write_text("Test text.\n")
    test_file_content = test_file.read_text()
    print("Test file content:")
    print(test_file_content)


if __name__ == '__main__':
    try:
        using_path_lib()
    except Exception as error:
        print(f"Unexpected error: {error}")
