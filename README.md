# Book-Tracker
#### **<ins>Description:**<ins>

This project consists of 4 files:
- book_tracker.py
- test_book_tracker.py
- requirements.txt
- README.md

The program is a **"Book Tracker"** with which one can add books to their library, view the library books and get various statistics about them.

The book information is stored in a CSV file called `"library_username.csv"`.
Each row in the file corresponds to a book and its specific information (title, author, pages etc.)

---

#### **<ins>Usage:<ins>**

`python book_tracker.py`

This program is an "Interactive console program" and functions through `input()`.

The whole program can be stopped at any time by pressing `Ctrl + C` or `Ctrl + D`.

After starting the game, one is asked for a username. Under this name, all the book information will be stored in the user library (the CSV file).

---

#### **<ins>Features:<ins>**
- adding a book to the library
- viewing the library
- deleting a book from the library
- seeing statistics about the books
- updating the reading status of a book

---

#### **<ins>Functioning:<ins>**

In project.py there are 15 functions, including the `main()` function.

The script starts off by importing different libraries, listed in the requirements.txt file.

<br>

As the program starts, a welcome message is printed and the `usernamer()` as well as the `main()` function are called through the main guard.

The first function is `usernamer()` which fulfills the purpose of asking the user for a username that is required for identifying the user and linking them to their correct library CSV file.

The `main()` function determines whether the user wants to:
- add a book to the library -> `add()`
- view the library -> `library()`
- delete a book from the library -> `delete()`
- see statistics about the books -> `stats()`
- update the reading status of a book -> `update_book()`

This function is called is also called in the `write()`, `library()`, `delete()`, `stats()`, `update_timeline()` and `update_book()`function.

The `write()` function is responsible for writing the CSV files as well as distributing the right information per user and book.
Headers of the CSV file:
- title
- author
- pages
- genre
- kind -> "Print" or "Ebook"
- stars -> rating of the book
- start
- finish
- days read -> days it took to finish the book
- status -> to be read/currently reading/did not finish/done
- notes

Another very important function is `add()` where all the book information is gathered from user input.
"Title", "Author", "Pages", "Genre" and "Kind" are mandatory fields to be filled out.
The "optional" fields are determined in the `status()` function.
If "start" and "finish" are given, the days it took to finish the book are calculated, the user rates the book in "stars" and can write their thoughts about the book in the "notes" field. The "status" is then switched to "Done" in the `done()` function.
If only "start" is given, the "status" is switched to "CR" (currently reading) in the `cr()` function.
If neither "start" nor "finish" are given, the "status" is immedietly switched to "TBR" (to be read) in the `tbr()` function.
If "DNF" is filled in the "finish" field, the "status" is switched to "DNF" (did not finish) in the `dnf()` function.

The `library()` function shows the user their library books divided into 4 categories (TBR, CR, DNF and Done) by the `update_timeline()` function.

If the user wanted to delete a book from their library, `delete()` would be called. The corresponding row for the book in the CSV file is then removed.

The function `easier()` provides a generalized template for the `stats()` function to calculate the number of books started or finished within each month or year.

If the user wants to see statistics about the books in their libraries, `stats()` is called.
Statistics:
1. Amount of books by author
2. Amount of books in genre ...
3. Page statistic
4. Amount of ebooks and prints in library
5. Book rating statistic
6. Amount of books started in (month/year)
7. Amount of books finished in (month/year)
8. Days statistic
9. Current book statuses

Another function is `update_timeline()`. It updates the "timeline" of the CSV file. That means the rows are ordered of when the book was finished/started. The function is called in `library()` and `stats()`.

The last function is the `update_book()` function which can be called in the `main()` function through user input. It lets the user update the reading status of their books (TBR->CR->Done/DNF).

<br>


