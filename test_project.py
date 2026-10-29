import project
from unittest.mock import patch

def test_done():
    project.username, project.name = "testuser", "testuser"

    def test_done_calls_main():
        with patch("project.main") as mock_main:
            assert project.done("Test_title", "Test_author", "234", "Test_genre", "Ebook", 5, "05-10-2025", "07-10-2025", 2, "NICE") == project.write("testuser", "Test_title", "Test_author", "234", "Test_genre", "Ebook", 5, "05-10-2025", "07-10-2025", 2, "Done", "NICE")
            assert project.done("22", "Author", "2342", "Romance", "Ebook", 5, "05-12-2025", "07-12-2025", 2, "Great") == project.write("testuser", "22", "Author", "2342", "Romance", "Ebook", 5, "05-12-2025", "07-12-2025", 2, "Done", "Great")
            assert project.done("Dont You", "Taylor", "0", "Fantasy", "Ebook", 3, "23-02-2026", "27-02-2026", 4, "Okay") == project.write("testuser", "Dont You", "Taylor", "0", "Fantasy", "Ebook", 3, "23-02-2026", "27-02-2026", 4, "Done", "Okay")

        mock_main.assert_called_once()

def test_add():
    inputs = [
        "",
        "test_title",

        "",
        "test_author",

        "abc",
        "hello",
        "12abc",
        "123",

        "",
        "test_genre",

        "",
        "   ",
        "Print",

        "abc",
        "123",
        "01-10-2026",

        "wrong",
        "32/10/2026",
        "04-10-2026"]

    with patch("builtins.input", side_effect=inputs):
        with patch("project.status") as mock_status:

            project.add()

            mock_status.assert_called_once_with(
                "Test_Title",
                "Test_Author",
                "123",
                "Test_Genre",
                "Print",
                "01-10-2026",
                "04-10-2026",
            )

def test_status():
    project.username = "testuser"

    def test_status_calls_main():
        with patch("project.main") as mock_main:

            #tbr
            assert project.status("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", "", "") == project.tbr("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook")
            assert project.status("Book Title", "Author Name", "42345", "Romance", "Print", "", "") == project.tbr("Book Title", "Author Name", "42345", "Romance", "Print")
            assert project.status("Another Title", "Cool Author", "1", "Fantasy", "Ebook", "", "") == project.tbr("Another Title", "Cool Author", "1", "Fantasy", "Ebook")

            #dnf
            assert project.status("Test_Title", "Test_Author", "234", "Test_Genre", "Print", "05-10-2025", "dnf") == project.dnf("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", "05-10-2025")
            assert project.status("Hello", "Taylor", "234", "Thriller", "Ebook", "28-01-2020", "dnf") == project.dnf("Hello", "Taylor", "234", "Thriller", "Ebook", "28-01-2020")
            assert project.status("Another Title", "Author Name", "234", "Great G", "Print", "05-05-2012", "dnf") == project.dnf("Another Title", "Author Name", "234", "Great G", "Print", "05-05-2012")

            #cr
            assert project.status("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", "27-07-2024", "") == project.cr("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", "27-07-2024")
            assert project.status("Nice Title", "Nice Author", "0", "Genre", "Ebook", "09-07-2023", "") == project.cr("Nice Title", "Nice Author", "0", "Genre", "Ebook", "09-07-2023")
            assert project.status("A Title", "An Author", "3431513", "Cool Genre", "Print", "11-12-2022", "") == project.cr("A Title", "An Author", "3431513", "Cool Genre", "Print", "11-12-2022")

            #done
            inputs = [4, "GREAT"]
            with patch("builtins.input", side_effect=inputs):
                result = project.status("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", "27-07-2024", "28-07-2024")
            assert result == project.done("Test_Title", "Test_Author", "234", "Test_Genre", "Ebook", 4, "27-07-2024", "28-07-2024", 1, "GREAT")
            inputs = [3, "Nice Book"]
            with patch("builtins.input", side_effect=inputs):
                result = project.status("Another Title", "Author Name", "234", "Great G", "Print", "05-05-2012", "25-05-2012")
            assert result == project.done("Another Title", "Author Name", "234", "Great G", "Print", 3, "05-05-2012", "25-05-2012", 20, "Nice Book")
            inputs = [5, "Fantastic Read"]
            with patch("builtins.input", side_effect=inputs):
                result = project.status("Hello", "Taylor", "234", "Thriller", "Ebook", "28-01-2020", "28-01-2020")
            assert result == project.done("Hello", "Taylor", "234", "Thriller", "Ebook", 5, "28-01-2020", "28-01-2020", 1, "Fantastic Read")

        mock_main.assert_called_once()


