from functions.get_file_content import get_file_content


def test_get_file_content():
    result = get_file_content("calculator", "lorem.txt")
    print(result, "\n")

    result = get_file_content("calculator", "main.py")
    print(result, "\n")

    result = get_file_content("calculator", "pkg/calculator.py")
    print(result, "\n")

    # Should return an error
    result = get_file_content("calculator", "/bin/cat")
    print(result, "\n")

    # Should return an error
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result, "\n")


if __name__ == "__main__":
    test_get_file_content()
