"""
This python code creates an SQL database and then
interacts and modifies the data within the database.
"""

# === IMPORT MODULES ===
import sqlite3


# === FUNCTIONS SECTION ===
def create_tbl(cursor_func):
    """
    This function creates a table for a bookstore and inserts
    collections of data within the table
    """

    # Create the table
    cursor_func.execute('''CREATE TABLE {}
       (id INTEGER NOT NULL,
       Title TEXT,
       Author INTEGER,
       Qty INTEGER,
       PRIMARY KEY (id))'''.format(table_name))

    # Create list with data to insert into table
    book_list = [
        (3001, "A Tale of Two Cities".title(), "Charles Dickens".title(), 30),
        (3002, "Harry Potter and the Philosopher's Stone".title(), "J.K. Rowling".title(), 40),
        (3003, "THe Lion, the Witch and the Wardrobe".title(), "C.S.Lewis".title(), 25),
        (3004, "The Lord of the Rings".title(), "J.R.R Tolkein".title(), 37),
        (3005, "Alice in Wonderland".title(), "Lewis Carroll".title(), 12),
        (3006, "James and the Giant Peach".title(), "Roald Dahl".title(), 67),
        (3007, "The Girl with the Dragon Tattoo".title(), "Steig Larsson".title(), 12),
        (3008, "Charlie and the Chocolate Factory".title(), "Roald Dahl".title(), 25),
        (3009, "Wagh".title(), "Prince Harry".title(), 5)
    ]

    # Insert list into table
    cursor_func.executemany(''' INSERT INTO {} VALUES
           (?,?,?,?)'''.format(table_name), book_list)


def init_db():
    """
    This function tries to connect to a database and creates a cursor object to handle it.
    Function also checks if a specific table name already exists within the database.
    create_tbl function is called if table does not exist.
    """

    # Main try-except block to connect to database and creates a cursor object
    try:
        # Connect to database
        db_func = sqlite3.connect(db_name)

        # Get cursor object
        cursor_func = db_func.cursor()

        # Nested try except block checks if table already exists within database
        # If it doesn't, create the database
        try:
            cursor_func.execute('''SELECT * FROM {}'''.format(table_name))

        # Create table within database
        except sqlite3.OperationalError:
            create_tbl(cursor_func)
            # Commit changes to db
            db_func.commit()

    # Raise error thrown when trying to connect to database
    except Exception as e:
        raise e

    # Return database and cursor
    return db_func, cursor_func


def add_book():
    """
    The aim of this function is to add a book to the table within the database.
    Firstly, the correct rowID is obtained.
    Secondly, the user submits title, author and quantity.
    Each input is checked.
    Then a search is conducted to ensure the new book doesn't already exist within the table.
    Lastly, the new book is added to the table, then committed to the database
    """
    # get ID for new book, add 1 from last row of table
    last_id = cursor.execute(''' SELECT MAX(id) FROM {} '''.format(table_name)).fetchall()
    new_id = last_id[0][0] + 1

    # === Get new book title ===
    input_str = "Please enter the title of the book to be added? "
    new_title = check_input(input_str)

    # === Get new book author
    input_str = "Please enter the author of the book to be added? "
    new_author = check_input(input_str)

    # === Get new book quantity ===
    input_str = "Please enter the quantity of the new book? "
    new_quant = menu_input_check(input_str)

    # === Check if book already exists in database
    search = search_table("id", "Title", new_title, "AND", "Author", new_author)

    # If an id is returned, display this to the user
    if len(search) > 0:
        print_warning(f"\nBook already exists, ID:{search[0][0]}")
        print_error("Book not added")
        return

    # === Insert book into table ===
    cursor.execute(''' INSERT INTO {} VALUES
           (?,?,?,?)'''.format(table_name), (new_id, new_title, new_author, new_quant))

    # Commit changes to database
    db.commit()

    # Print success message
    print_confirm(f"{new_title} added to table: {table_name} ")


def update_book():
    """
    Function updates a book within the database.
    Function begins asking what row ID the user would like to update.
    Then what book attribute the user would like to update.
    Finally, the function passes onto the update_table function which sends the required
    SQL commands to the database
    :return: nothing
    """

    # While loop to confirm which row ID is to be updated
    while True:

        # Create input message
        input_str = f"\nEnter the ID of the book you would like to update, " \
                    f"enter 0 to view all, or -1 to return to menu."

        # check input and convert to integer
        update_id = menu_input_check(input_str)

        # If user entered 0, run view all
        if update_id == 0:
            view_all()
            continue

        # Else if user wants to return to menu, exit function
        elif update_id == "-1":
            return

        # Else, check ID exists within table
        else:
            # Search all SQL command
            attribute = '*'
            # View attribute sends required SQL commands
            check_func = view_attribute(attribute, update_id)

            # If an id is not returned, continue loop
            if check_func is None:
                continue

            # Else break and carry on
            else:
                break

    # Create menu display to determine which attribute user would like to update
    update_disp = f"\n──────[{update_id} SELECTED]────────────\n"
    update_disp += f"\n"
    update_disp += f"Which attribute would you like to update?\n"
    update_disp += f"1\t-\tTitle\n"
    update_disp += f"2\t-\tAuthor\n"
    update_disp += f"3\t-\tQuantity\n"
    update_disp += f"0\t-\tReturn to Menu\n"
    update_disp += f"─────────────────────────────────\n"

    # While loop determines what attribute user would like to update
    while True:

        # Get input from user
        update_choice = menu_input_check(update_disp)

        # Update title
        if update_choice == 1:
            attribute = "Title"

        # Update Author
        elif update_choice == 2:
            attribute = "Author"

        # Update Quantity
        elif update_choice == 3:
            attribute = "Qty"

        # Return to menu
        elif update_choice == 0:
            return

        else:
            print(f"{update_choice} is not an option. Please try again")
            continue

        # Update SQL Entry
        update_table(attribute, update_id)
        return


def del_book():
    """
    Function requests the rowID of the book to be deleted from the user.
    Function then searches for the title of that rowID.
    This confirms the book exists and provides data from a confirmation message.
    Finally, SQL command is sent to database to delete the database entry.
    :return: Nothing.
    """

    # While loop to confirm which row ID is to be deleted
    while True:

        # Create input message
        input_str = f"\nEnter the ID of the book you would like to delete, " \
                    f"enter 0 to view all, or -1 to return to menu."

        # check input and convert to integer
        del_id = menu_input_check(input_str)

        # If user entered 0, run view all
        if del_id == 0:
            view_all()
            continue

        # Else if user wants to return to menu, exit function
        elif del_id == "-1":
            return

        # Else, check ID exists within table
        else:
            # Search SQL command
            attribute = 'Title'
            # View attribute sends required SQL commands
            check_func = view_attribute(attribute, del_id)

            # If an id is not returned, continue loop
            if check_func is None:
                continue

            # Else break and carry on
            else:

                while True:
                    # Confirm with user
                    del_check = input(f"Are you sure you want to delete {check_func}"
                                      f" from the database? (y/n) ").lower()

                    # If user doesn't confirm delete, return user to main menu
                    if del_check == "n":
                        return

                    # If user confirms, break loop
                    elif del_check == "y":
                        break

                    # Otherwise input not recognised
                    else:
                        print_warning(f"\n{del_check} was not recognised. Please try again")

                # Send delete SQL query
                cursor.execute(''' DELETE FROM {} WHERE id = ?'''
                               .format(table_name), (del_id,))

                # Commit change to database
                print_confirm(f"\n{check_func} deleted.")
                db.commit()

                # Return to exit while loop
                return


def search_book():
    """
    This function determines what attribute the user would like to search for, then the search query itself.
    The function then passes the information to another function which executes the SQL search.
    Finally, the function passes the search result to a function which prints the result to the console.
    :return: Nothing
    """

    # Create menu display
    search_disp = f"─────────────────────────────────\n"
    search_disp += f"\n"
    search_disp += f"What attribute would you like to search for?\n"
    search_disp += f"1\t-\tRow ID\n"
    search_disp += f"2\t-\tTitle\n"
    search_disp += f"3\t-\tAuthor\n"
    search_disp += f"4\t-\tQuantity\n"
    search_disp += f"0\t-\tReturn to Menu\n"
    search_disp += f"─────────────────────────────────\n"

    # Pass menu to function which checks the input
    search_choice = menu_input_check(search_disp)

    # While loop ensures input is an option
    while True:
        if search_choice == 0:
            return

        elif search_choice == 1:
            attribute = "id"

        elif search_choice == 2:
            attribute = "Title"

        elif search_choice == 3:
            attribute = "Author"

        elif search_choice == 4:
            attribute = "Qty"

        else:
            print_warning(f"{search_choice} is not an option. Please try again")
            continue

        # Get search query from the user
        att_disp = f"Please enter you search query\n"
        search_attribute = check_input(att_disp)

        # === Check if book already exists in database, the following function executes the SQL commands.
        search = search_table("*", attribute, search_attribute)

        if len(search) == 0:
            print_warning(f"\nNothing found for search: {search_attribute}")

        else:
            # Print results to screen
            table_print(search)

        return


def search_table(att_output: str, att_input_01: str, att_01_search: str,
                 logical=None, att_input_02=None, att_02_search=None):
    """
    This function executes the SQL search commands and returns the output
    :param att_output: Attribute the user wants from the search query
    :param att_input_01: What attribute to search for first
    :param att_01_search: Search value for first attribute
    :param logical: AND / OR logical operator
    :param att_input_02: What attribute to search for second
    :param att_02_search: Search value for second attribute
    :return: List of results from SQL search command
    """

    # If single attribute search criteria has been requested
    if att_input_02 is None:
        output = cursor.execute(''' SELECT {} FROM {} WHERE {} = ?'''
                                .format(att_output, table_name, att_input_01), (att_01_search,)).fetchall()

    # Else multiple search criteria has been requested
    else:
        output = cursor.execute(''' SELECT {} FROM {} WHERE {} = ? {} {} = ?'''
                                .format(att_output, table_name, att_input_01, logical, att_input_02),
                                (att_01_search, att_02_search)).fetchall()
    # Return search results
    return output


def view_all():
    """
    This function selects all entries within the table.
    It then prints using the "tabulate" module.
    """
    # Query SQL
    results = cursor.execute(''' SELECT * FROM {} '''.format(table_name)).fetchall()
    # Send to table print function
    table_print(results)


def view_attribute(attribute: str, id_func: int):
    """
    This function obtains a particular attribute from an SQL table
    :param attribute: attribute to obtain a value for. Must be a string
    :param id_func: row ID of the table entry. Must be a string
    :return: resulting value
    """

    # Try block captures an errors
    try:
        # Query SQL
        result = cursor.execute(''' SELECT {} FROM {} WHERE id = ?'''
                                .format(attribute, table_name), (id_func,)).fetchall()[0][0]
        return result

    # Raise an exception and rollback changes
    except IndexError:
        print_error("ID does not exist")
        return None

    except Exception as e:
        db.rollback()
        raise e


def update_table(attribute: str, update_id: int):
    """
    This function shows the user what the current attribute value is within the database table.
    Then confirms the new value.
    Then finally the function updates the attribute.
    :param attribute: attribute (or table column) to be changed
    :param update_id: rowID
    """

    # Show user the current attribute value in the table
    current_value = view_attribute(attribute, update_id)
    print(f"The current {attribute} is {current_value}")

    input_str = f"Please enter the new {attribute.lower()} "

    update_value = check_input(input_str)

    # Try block captures an errors when executing SQL commands
    try:
        cursor.execute(''' UPDATE {} SET {} = ? WHERE id = ?'''
                       .format(table_name, attribute), (update_value, update_id))

        print_confirm("\nUpdate successful")
        db.commit()

    # Raise an exception and rollback changes
    except Exception as e:
        db.rollback()
        raise e


def table_print(table, headers=[]):
    """
    Function prints to console using tabulate module
    """

    # Import modules
    from tabulate import tabulate

    # If headers list is empty, make headers default
    if not headers:
        headers = ["ID", "Title", "Author", "Quantity"]

    print(f"\n")
    print(tabulate(table, headers, tablefmt="simple"))


def menu_input_check(menu: str):
    """
   This function ensures the user has entered an integer and returns an integer.
   A user may enter -1 to indicate they want to go back to the main menu.
   Therefore, a input of -1 will be returned without conversion to an integer
   :param menu: menu to be displayed to the user
   :return: integer
   """

    while True:
        user_input = input(menu)

        # Check if input is -1
        if user_input == "-1":
            return user_input

        # check input is an integer
        else:
            check_func = int_check(user_input)

        # If check function returns false, user did not input an integer
        # Print message and continue while loop
        if not check_func:
            continue
        # Else convert user input to integer
        else:
            user_input = int(user_input)
            return user_input


def int_check(input_int: str) -> bool:
    """
    This function checks if an input is an integer
    Function returns True if the input is an integer
    """
    # Initialise boolean
    check_func = False
    # isnumeric method use to confirm input is part of alphabet
    if input_int.isnumeric():
        # Set boolean to true
        check_func = True

    else:
        # print message
        print_warning(f"\n{input_int} is not an recognised, please try again.")

    # return boolean
    return check_func


def check_input(input_string: str) -> str:
    """
    Function asks user to confirm their choice
    :param input_string: Answer to be checked
    :return: Return value if user confirms answer
    """
    # While loop confirms updated value
    while True:

        # Get input value from user
        value = input(input_string).title()

        # Confirm input with user
        check_func = user_continue(value)

        # If user_continue function returns false, repeat while loop
        if not check_func:
            continue

        else:
            return value


def user_continue(func_input) -> bool:
    """
    This function prints a users input back to the console for confirmation.
    Returns a boolean which confirms
    """

    while True:

        # Request input from user
        user_input = input(f"{func_input} was inputted. Is this correct? (y/n)? ").lower()

        # If user input is yes, return True
        if user_input == "y":
            check = True
            return check

        # If user input is no, return False
        elif user_input == "n":
            check = False
            return check

        # Else input is not recognised
        else:
            print_warning("Input not recognised. Please try again")
            continue


def print_error(input_str):
    """
    Function prints input_str to console in colour red
    :param input_str: string
    :return: nothing
    """

    lightred = '\033[91m'
    white = '\033[00m'
    print(f"{lightred}{input_str}{white}")


def print_warning(input_str):
    """
    Function prints input_str to console in colour yellow
    :param input_str: string
    :return: nothing
    """

    yellow = '\033[93m'
    white = '\033[00m'
    print(f"{yellow}{input_str}{white}")


def print_confirm(input_str):
    """
    Function prints input_str to console in colour green
    :param input_str: string
    :return: nothing
    """

    green = '\033[92m'
    white = '\033[00m'
    print(f"{green}{input_str}{white}")


# === INITIALISE ====
# Define database name
db_name = 'ebookstore'

# Define table name
table_name = 'books'

# Initialise database and table
db, cursor = init_db()

# Create menu display
menu_disp = f"\n"
menu_disp += f"─────────────[MENU]─────────────\n"
menu_disp += f"Select one of the following options below:\n"
menu_disp += f"1\t-\tEnter new book\n"
menu_disp += f"2\t-\tUpdate book\n"
menu_disp += f"3\t-\tDelete book\n"
menu_disp += f"4\t-\tSearch books\n"
menu_disp += f"5\t-\tView all books\n"
menu_disp += f"0\t-\tExit\n"
menu_disp += f"─────────────────────────────────\n"

# === MAIN BODY ===
while True:

    # Get user choice
    user_choice = menu_input_check(menu_disp)

    # === Add a book to the database ===
    if user_choice == 1:
        add_book()

    # === Update the information about a book ===
    elif user_choice == 2:
        update_book()

    # === Delete a book within the database ===
    elif user_choice == 3:
        del_book()

    # === Search for a book within the database ===
    elif user_choice == 4:
        search_book()

    # === Search for a book within the database ===
    elif user_choice == 5:
        view_all()

    # === Exit the program ===
    elif user_choice == 0:
        db.close()
        print('Goodbye!!!')
        exit()

    else:
        print_warning(f"\n{user_choice} is not an option. Please try again")
        continue
