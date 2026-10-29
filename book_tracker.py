from sys import exit
import csv
from datetime import datetime
from os.path import getsize
from re import fullmatch
from itertools import chain
from operator import itemgetter
import calendar

def usernamer():
    try:
        username = ""
        while not username or username == " ":
            username = input("What's your name? ").lower().replace(" ", "")
        return username
    except (EOFError, KeyboardInterrupt):
        exit("\n\nProgramm stopped.\n")

def main():
    global username
    username = name
    try:
        while True:
            dec = input("\n1. Add book\n2. View library\n3. Delete book\n4. Stats\n5. Update book\n=> ").lower()
            if dec in ["1", "1.", "add book", "1. add book"]:
                return add()
            elif dec in ["2", "2.", "view library", "2. view library"]:
                return library(username)
            elif dec in ["3", "3.", "delete book", "3. delete book"]:
                return delete(username)
            elif dec in ["4", "4.", "stats", "4. stats"]:
                return stats(username)
            elif dec in ["5", "5.", "update book", "5. update book"]:
                return update_book(username)
            else:
                print("\nInvalid input.")
                continue
    except (EOFError, KeyboardInterrupt):
        exit("\n\nProgramm stopped.\n")

def write(username, title, author, pages, genre, kind, stars, start, finish, days, status, notes):
    name = f"library_{username}.csv"
    with open(name, "a+") as f:
        writer = csv.writer(f)
        if getsize(name) == 0:
            writer.writerow(["Title", "Author", "Pages", "Genre", "Kind", "Stars", "Start", "Finish", "Days Read", "Status", "Notes"])
        writer.writerow([title, author, pages, genre, kind, stars, start, finish, days, status, notes])

    main()

def status(title, author, pages, genre, kind, start, finish):
    if fullmatch(r" +|", start) and fullmatch(r" +|", finish):
        tbr(title, author, pages, genre, kind)
    if fullmatch(r"(^\d{2}-\d{2}-\d{4}$)", start) and fullmatch(r"(^\d{2}-\d{2}-\d{4}$)|DNF|dnf", finish):
        if finish == "DNF" or finish == "dnf":
            dnf(title, author, pages, genre, kind, start)
        else:
            start_date = datetime.strptime(start, "%d-%m-%Y")
            finish_date = datetime.strptime(finish, "%d-%m-%Y")
            days = (finish_date - start_date).days
            print(f"=> Total number of days read: {days}")

            while True:
                try:
                    stars = float(input("Stars (1-5): "))
                    if float(stars) < 1 or float(stars) > 5:
                        raise ValueError
                    break
                except ValueError:
                    continue
            notes = input("Notes: ")

            done(title, author, pages, genre, kind, stars, start, finish, days, notes)
    if fullmatch(r"(^\d{2}-\d{2}-\d{4}$)", start) and fullmatch(r" +|", finish):
        cr(title, author, pages, genre, kind, start)
    while fullmatch(r" +|", start) and fullmatch(r"(^\d{2}-\d{2}-\d{4}$)", finish):
        print("You can't finish a book without starting it first.")
        while True:
            try:
                start, finish = "wrong", "wrong"
                while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +|", start):
                    start = input("Started on (DD-MM-YYYY): ")
                while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +||DNF|dnf", finish):
                    finish = input("Finished on (DD-MM-YYYY): ")
                break
            except ValueError:
                continue

def tbr(title, author, pages, genre, kind):
    status = "TBR"
    write(username, title, author, pages, genre, kind, "", "", "", "", status, "")

def cr(title, author, pages, genre, kind, start):
    status = "CR"
    write(username, title, author, pages, genre, kind, "", start, "", "", status, "")

def dnf(title, author, pages, genre, kind, start):
    status = "DNF"
    write(username, title, author, pages, genre, kind, "", start, "", "", status, "")

def done(title, author, pages, genre, kind, stars, start, finish, days, notes):
    status = "Done"
    write(username, title, author, pages, genre, kind, stars, start, finish, days, status, notes)

def add():
    try:

        print("\n\033[1;4mBook:\033[0m\n")
        title, author, pages, genre, kind = "", "", "", "", ""
        while not title or title.isspace() == True:
            title = input("Title: ").title()
        while not author or author.isspace() == True:
            author = input("Author: ").title()
        while pages.isdigit() == False:
            pages = input("Pages: ")
        while not genre or genre.isspace() == True:
            genre = input("Genre: ").title()
        while kind != "Print" and kind != "Ebook":
            kind = input("\"Print\" or \"Ebook\": ").title()

        while True:
            try:
                start, finish = "wrong", "wrong"
                while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +|", start):
                    start = input("Started on (DD-MM-YYYY): ")
                while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +||DNF|dnf", finish):
                    finish = input("Finished on (DD-MM-YYYY): ")
                break
            except ValueError:
                continue

        status(title, author, pages, genre, kind, start, finish)

    except (EOFError, KeyboardInterrupt):
        exit("\n\nProgramm stopped.\n")

def library(username):
    try:

        done_rows, tbr_rows, cr_rows, dnf_rows = update_timeline(username)

        print("\n\033[1;4mTBR - To Be Read\033[0m\n")
        for i, row in enumerate(tbr_rows, start=1):
            print(f"{i}.\n{row[0]} by {row[1]}:\n",
                    f"{row[2]} pages\n",
                    f"Genre: {row[3]}\n",
                    f"Kind: {row[4]}")

        print("\n\033[1;4mCR - Currently Reading\033[0m\n")
        for i, row in enumerate(cr_rows, start=1):
            print(f"{i}.\n{row[0]} by {row[1]}:\n",
                    f"{row[2]} pages\n",
                    f"Genre: {row[3]}\n",
                    f"Kind: {row[4]}\n",
                    f"Started on: {row[6]}\n")

        print("\n\033[1;4mDNF - Did Not Finish\033[0m\n")
        for i, row in enumerate(dnf_rows, start=1):
            print(f"{i}.\n{row[0]} by {row[1]}:\n",
                    f"{row[2]} pages\n",
                    f"Genre: {row[3]}\n",
                    f"Kind: {row[4]}\n",
                    f"Started on: {row[6]}\n")

        print("\n\033[1;4mDone - Completed\033[0m\n")
        for i, row in enumerate(done_rows, start=1):
            print(f"{i}.\n{row[0]} by {row[1]}:\n",
                    f"{row[2]} pages\n",
                    f"Genre: {row[3]}\n",
                    f"Kind: {row[4]}\n",
                    f"Stars: {row[5]}\n",
                    f"Started on: {row[6]}\n",
                    f"Finished on: {row[7]}\n",
                    f"=> Total number of days read: {row[8]}\n",
                    f"Notes: {row[10]}\n")

        count = len(done_rows) + len(tbr_rows) + len(cr_rows) + len(dnf_rows)
        if count == 1:
            print(f"\n=> There is \033[1;4m{count}\033[0m book in your library.\n")
        else:
            print(f"\n=> There are \033[1;4m{count}\033[0m books in your library.\n")

        main()

    except (EOFError, KeyboardInterrupt):
            exit("\n\nProgramm stopped.\n")

def delete(username):
    try:

        with open(f"library_{username}.csv", "r+") as inp:
            reader = csv.reader(inp)
            header = next(reader)
            rows = list(reader)

            books = []

            print("\nAll books in your library (Title by author):\n")
            for i, book in enumerate(rows, start=1):
                print(f"{i}. {book[0]} by {book[1]}")
                books.append({"number": i, "title": book[0], "author": book[1]})

            delete_book = ""
            while delete_book.isdigit() == False:
                delete_book = input("\nWhich book do you want to delete? \nType in the corresponding number.\n=> ")

            for book in books:
                if book["number"] == int(delete_book):
                    delete_title = book["title"]
                    delete_author = book["author"]

            new_rows = []

            for row in rows:
                if row[0] != delete_title and row[1] != delete_author:
                    new_rows.append(row)
                else:
                    print(f"{row[0]} by {row[1]} was deleted from your library.")

        with open(f"library_{username}.csv", "w") as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(new_rows)

        main()

    except (EOFError, KeyboardInterrupt):
            exit("\n\nProgramm stopped.\n")

def easier(months_years, number, month_year):

    name = f"library_{username}.csv"
    with open(name) as f:

        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

        if number == 6:
            print(f"\n\033[1;4mBooks that were started in {month_year} ...:\033[0m")
        else:
            print(f"\n\033[1;4mBooks that were finished in {month_year} ...:\033[0m")

        months_years = []

        for row in rows:
            if row[number] != "":
                var = int(getattr(datetime.strptime(row[number], "%d-%m-%Y"), month_year))
                if var not in months_years:
                    months_years.append(var)

        for variable in sorted(months_years):
            titles_authors = []
            for row in rows:
                if row[number] != "":
                    var = int(getattr(datetime.strptime(row[number], "%d-%m-%Y"), month_year))
                    if var == variable:
                        titles_authors.append(f"{row[0]} by {row[1]}")

            if month_year == "month":
                print(f"\n\033[1;4m{calendar.month_name[variable]}\033[0m:")
            else:
                print(f"\n\033[1;4m{variable}\033[0m:")
            for i, title_author in enumerate(titles_authors, start=1):
                print(f"{i}. {title_author}")

def stats(username):
    try:

        name = f"library_{username}.csv"
        with open(name) as f:
            if getsize(name) == 0:
                print("You need to add books to your library first.")
                main()

            reader = csv.reader(f)
            next(reader)

            while True:
                dec = input("\nWhat kind of stats do you want to know:\n1. Amount of books by author\n2. Amount of books in genre ...\n3. Page statistic\n4. Amount of ebooks and prints in library\n5. Book rating statistic\n6. Amount of books started in (month/year)\n7. Amount of books finished in (month/year)\n8. Days statistic\n9. Current book statuses\n=> ")
                if dec in ["1", "1.", "amount of books by author", "1. amount of books by author"]:

                    authors = []

                    rows = list(reader)

                    for row in rows:
                        if row[1] not in authors:
                            authors.append(row[1])

                    for author in authors:
                        titles = []
                        for row in rows:
                            if row[1] == author:
                                titles.append(row[0])
                        print(f"\n\033[1;4m{author}\033[0m:")
                        for i, title in enumerate(titles, start=1):
                            print(f"{i}. {title}")


                elif dec in ["2", "2.", "amount of books in genre ...", "2. amount of books in genre ..."]:

                    genres = []

                    rows = list(reader)

                    for row in rows:
                        if row[3] not in genres:
                            genres.append(row[3])

                    for genre in genres:
                        titles_authors = []
                        for row in rows:
                            if row[3] == genre:
                                titles_authors.append(f"{row[0]} by {row[1]}")
                        print(f"\n\033[1;4m{genre}\033[0m:")
                        for i, title_author in enumerate(titles_authors, start=1):
                            print(f"{i}. {title_author}")

                elif dec in ["3", "3.", "page statistic", "3. page statistic"]:
                    pages_data = []

                    print("")

                    for row in reader:
                        pages_data.append({"pages": int(row[2]), "title": row[0], "author": row[1]})

                    final_pages = sorted(pages_data, key=itemgetter("pages"), reverse=True)

                    for i, page in enumerate(final_pages, start=1):
                        print(f"{i}. {page["pages"]}: {page["title"]} by {page["author"]}")

                elif dec in ["4", "4.", "amount of ebooks and prints in library", "4. amount of ebooks and prints in library"]:
                    ebooks = []
                    prints = []
                    for row in reader:
                        if row[4] == "Ebook":
                            ebooks.append(f"{row[0]} by {row[1]}")
                        else:
                            prints.append(f"{row[0]} by {row[1]}")
                    print("\n\033[1;4mEbooks\033[0m\n")
                    for i in ebooks:
                        print(i)
                    print(f"=> Ebooks: {len(ebooks)}")
                    print("\n\033[1;4mPrints\033[0m\n")
                    for i in prints:
                        print(i)
                    print(f"=> Prints: {len(prints)}")

                elif dec in ["5", "5.", "book rating statistic", "5. book rating statistic"]:
                    stars_data = []
                    for row in reader:
                        if row[9] == "Done":
                            stars_data.append({"stars": row[5], "title": row[0], "author": row[1]})

                    final_stars = sorted(stars_data, key=itemgetter("stars"), reverse=True)

                    print("")
                    for i, star in enumerate(final_stars, start=1):
                        print(f"{i}. {star["stars"]}: {star["title"]} by {star["author"]}")

                elif dec in ["6", "6.", "amount of books started in (month/year)", "6. amount of books started in (month/year)"]:
                    next_dec = input("\"Monthly\" or \"Yearly\" statistic: ").lower()
                    if next_dec in ["1", "month", "monthly"]:

                        easier(months_years="months",  number=6, month_year="month")

                    elif next_dec in ["2", "year", "yearly"]:

                        easier(months_years="years", number=6, month_year="year")

                    else:
                        print("\nInvalid input.")
                        continue
                elif dec in ["7", "7.", "amount of books finished in (month/year)", "7. amount of books finished in (month/year)"]:
                    next_dec = input("\"Monthly\" or \"Yearly\" statistic: ").lower()
                    if next_dec in ["1", "month", "monthly"]:

                        easier(months_years="months",  number=7, month_year="month")

                    elif next_dec in ["2", "year", "yearly"]:

                        easier(months_years="years", number=7, month_year="year")

                    else:
                        print("\nInvalid input.")
                        continue
                elif dec in ["8", "8.", "days statistic", "8. days statistic"]:
                    days_data = []

                    for row in reader:
                        if row[9] == "Done":
                            days_data.append({"days": float(row[8]), "title": row[0], "author": row[1]})

                    final_days = sorted(days_data, key=itemgetter("days"))

                    print("")
                    for i, day in enumerate(final_days, start=1):
                        print(f"{i}. {day["days"]}: {day["title"]} by {day["author"]}")

                elif dec in ["9", "9.", "current book statuses", "9. current book statuses"]:

                    done_rows, tbr_rows, cr_rows, dnf_rows = update_timeline(username)

                    print("\n\033[1;4mTBR - To Be Read\033[0m\n")
                    for i, row in enumerate(tbr_rows, start=1):
                        print(f"{i}. {row[0]} by {row[1]}")
                    print(f"TBR Books: {len(tbr_rows)}")

                    print("\n\033[1;4mCR - Currently Reading\033[0m\n")
                    for i, row in enumerate(cr_rows, start=1):
                        print(f"{i}. {row[0]} by {row[1]}")
                    print(f"CR Books: {len(cr_rows)}")

                    print("\n\033[1;4mDNF - Did Not Finish\033[0m\n")
                    for i, row in enumerate(dnf_rows, start=1):
                        print(f"{i}. {row[0]} by {row[1]}")
                    print(f"DNF Books: {len(dnf_rows)}")

                    print("\n\033[1;4mDone - Completed\033[0m\n")
                    for i, row in enumerate(done_rows, start=1):
                        print(f"{i}. {row[0]} by {row[1]}")
                    print(f"Finished Books: {len(done_rows)}")

                    count = len(done_rows) + len(tbr_rows) + len(cr_rows) + len(dnf_rows)
                    if count == 1:
                        print(f"\n=> There is \033[1;4m{count}\033[0m book in your library.\n")
                    else:
                        print(f"\n=> There are \033[1;4m{count}\033[0m books in your library.\n")
                else:
                    print("\nInvalid input.")
                    continue
                question = input("\nIf you want to continue displaying stats, press \"Enter\".\nIf you want to return to the main menu, type in \"Main\"\n=> ").lower()
                if question == "main":
                    main()
                else:
                    stats(username)

    except (EOFError, KeyboardInterrupt):
                exit("\n\nProgramm stopped.\n")

def update_timeline(username):
    try:

        name = f"library_{username}.csv"
        with open(name) as f:
            if getsize(name) == 0:
                print("You need to add books to your library first.")
                main()

            reader = csv.reader(f)
            next(reader)

            done_rows = []
            tbr_rows = []
            cr_rows = []
            dnf_rows = []

            for row in reader:
                if row[9] == "Done":
                    done_rows.append(row)
                elif row[9] == "TBR":
                    tbr_rows.append(row)
                elif row[9] == "CR":
                    cr_rows.append(row)
                else:
                    dnf_rows.append(row)

        done_rows.sort(key=lambda x:datetime.strptime(x[7], "%d-%m-%Y"))
        cr_rows.sort(key=lambda x:datetime.strptime(x[6], "%d-%m-%Y"))
        tbr_rows.sort(key=lambda x: x[0])
        dnf_rows.sort(key=lambda x: x[0])

        with open(f"library_{username}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Pages", "Genre", "Kind", "Stars", "Start", "Finish", "Days Read", "Status", "Notes"])

            all = list(chain(cr_rows, tbr_rows, done_rows, dnf_rows))

            for row in all:
                writer.writerow(row)

            return done_rows, tbr_rows, cr_rows, dnf_rows

    except (EOFError, KeyboardInterrupt):
                exit("\n\nProgramm stopped.\n")

def update_book(username):
    try:

        with open(f"library_{username}.csv", "r+") as inp:
            reader = csv.reader(inp)
            header = next(reader)
            rows = list(reader)

            books = []

            print("\nAll books in your library (Title by author):\n")
            for i, book in enumerate(rows, start=1):
                print(f"{i}. {book[0]} by {book[1]}")
                books.append({"number": i, "title": book[0], "author": book[1], "pages": book[2], "genre": book[3], "kind": book[4], "stars": book[5], "start": book[6], "finish": book[7], "days": book[8], "status": book[9], "notes": book[10]})

            edit_book = ""
            while edit_book.isdigit() == False:
                edit_book = input("\nWhich book do you want to edit? \nType in the corresponding number.\n=> ")

            for book in books:
                if book["number"] == int(edit_book):
                    delete_title = book["title"]
                    delete_author = book["author"]
                    print(f"\n\n{book["title"]} by {book["author"]}:\n",
                            f"{book["pages"]} pages\n",
                            f"Genre: {book["genre"]}\n",
                            f"Kind: {book["kind"]}\n",
                            f"Stars: {book["stars"]}\n",
                            f"Started on: {book["start"]}\n",
                            f"Finished on: {book["finish"]}\n",
                            f"=> Total number of days read: {book["days"]}\n",
                            f"Notes: {book["notes"]}\n")

                    if not book["finish"]:
                        if not book["start"]:
                            start = "wrong"
                            while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +|", start):
                                start = input("Started on (DD-MM-YYYY): ")
                        else:
                            start = book["start"]
                        finish = "wrong"
                        while not fullmatch(r"(^\d{2}-\d{2}-\d{4}$)| +||DNF|dnf", finish):
                            finish = input("Finished on (DD-MM-YYYY): ")
                    elif book["finish"] and book["start"]:
                        print("!Please make your edits manually in the csv file, as this program only allows you to update the reading status of your books (TBR->CR->Done/DNF)!")
                        main()

                    new_rows = []

                    for row in rows:
                        if row[0] != delete_title and row[1] != delete_author:
                            new_rows.append(row)

                    with open(f"library_{username}.csv", "w") as out:
                        writer = csv.writer(out)
                        writer.writerow(header)
                        writer.writerows(new_rows)

                    status(book["title"], book["author"], book["pages"], book["genre"], book["kind"], start, finish)

    except (EOFError, KeyboardInterrupt):
            exit("\n\nProgramm stopped.\n")


if __name__ == "__main__":
    try:
        print("\nWelcome to the \"BOOK TRACKER\"!!!")
        name = usernamer()
        main()
    except EOFError or KeyboardInterrupt:
        exit("\n\nProgramm stopped.\n")


