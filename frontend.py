from tkinter import Entry, Button, Tk, Label, END, Image, Listbox, StringVar, Scrollbar, Frame, messagebox, PhotoImage
from tkinter.ttk import *
from datetime import datetime
import backend


def get_selected_row(event):
    try:
        global selected_tuple
        index = books_list.curselection()[0]
        selected_tuple = books_list.get(index)
        entry_title.delete(0, END)
        entry_title.insert(END, selected_tuple[1])
        entry_author.delete(0, END)
        entry_author.insert(END, selected_tuple[2])
        year_Combo.delete(0, END)
        year_Combo.insert(END, selected_tuple[3])
        entry_isbn.delete(0, END)
        entry_isbn.insert(END, selected_tuple[4])
    except IndexError:
        pass


def view_command():
    books_list.delete(0, END)
    for row in backend.view():
        books_list.insert(END, row)
    clear_entry_widgets()


def search_command():
    books_list.delete(0, END)
    for row in backend.search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
        books_list.insert(END, row)


def add_command():
    if empty_entry_widgets() is True:
        pass
    elif validate_author(author_text) and validate_year(year_text) \
            and validate_isbn(isbn_text) and duplicate(isbn_text) is True:

        backend.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        books_list.delete(0, END)
        books_list.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))
        view_command()
    else:
        pass


def delete_command():
    backend.delete(selected_tuple[0])
    view_command()


def update_command():
    if empty_entry_widgets() is True:
        pass
    elif validate_author(author_text) and validate_year(year_text) \
            and validate_isbn(isbn_text)  is True:
        backend.update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        view_command()


def clear_command():
    books_list.delete(0, END)
    clear_entry_widgets()


def clear_entry_widgets():
    entry_title.delete(0, END)
    entry_author.delete(0, END)
    year_Combo.delete(0, END)
    entry_isbn.delete(0, END)


def empty_entry_widgets():
    if title_text.get() == '' and isbn_text.get() == '' and author_text.get() == '' and year_text.get() == '':
        messagebox.showerror("error", "Empty fields")
        return True
    elif title_text.get() == ' ' or isbn_text.get() == '' or author_text.get() == '' or year_text.get() == '':
        messagebox.showerror("error", "All Fields are Mandatory")
        return True
    else:
        return False


def validate_author(authortext):
    flag = 0
    for i in authortext.get():
        if i.isnumeric():
            flag += 1
    if flag != 0:
        messagebox.showerror("error", "Invalid Author Name")
        entry_author.delete(0, END)
        return False
    else:
        return True


def validate_year(yeartext):
    if len(yeartext.get()) == 4:
        if yeartext.get().isdigit():
            if start_from_year < int(year_text.get()) <= current_year:
                return True
            else:
                messagebox.showerror("error", "Books after year 2007  upto current year are only valid")
                year_Combo.delete(0, END)
                return False
        else:
            messagebox.showerror("error", "Invalid Year Entry")
            year_Combo.delete(0, END)
            return False
    else:
        messagebox.showerror("error", "Invalid Year Entry")
        year_Combo.delete(0, END)
        return False


def validate_isbn(isbntext):
    try:
        if len(isbntext.get()) != 13:
            messagebox.showerror("error", "Invalid ISBN Code")
            entry_isbn.delete(0, END)
            return False
        else:
            isbn_prefix = ""
            isbn_prefix = isbntext.get()[0] + isbntext.get()[1] + isbntext.get()[2]
            if int(isbn_prefix) == 978 or int(isbn_prefix) == 979:
                add = 0
                for i in range(12):
                    if 0 <= int(isbntext.get()[i]) <= 9:
                        if (i % 2) == 0:
                            add += int(isbntext.get()[i]) * 1
                        elif (i % 2) != 0:
                            add += int(isbntext.get()[i]) * 3
                if add % 10 != 0:
                    check_digit = 10 - (add % 10)
                    if check_digit == int(isbntext.get()[12]):
                        return True
                    else:
                        messagebox.showerror("error", "Invalid ISBN Code")
                        entry_isbn.delete(0, END)
                        return False
                else:
                    return True
            else:
                messagebox.showerror("error", "ISBN Code starts with prefix 978 or 979")
                entry_isbn.delete(0, END)
                return False
    except IndexError:
        pass


def duplicate(isbntext):
    count = 0
    for row in backend.isbn_duplicate():
        for i in row:
            if isbntext.get() in str(i):
                count += 1
    if count != 0:
        messagebox.showerror("error", "Information already existed")
        return False
    else:
        return True


window = Tk()
windowPadding = 16
window.title("BookStore")
window.configure(background="light blue")
window['padx'] = windowPadding
window['pady'] = windowPadding

label_title = Label(window, text="Title", font="arial 14", width=12, anchor='center', relief='ridge')
label_title.grid(row=0, column=0, pady=16)

label_author = Label(window, text="Author", font="arial 14", width=12, anchor='center', relief='ridge')
label_author.grid(row=0, column=2, pady=16)

label_year = Label(window, text="Year", font="arial 14", width=12, anchor='center', relief='ridge')
label_year.grid(row=1, column=0, pady=16)

label_isbn = Label(window, text="ISBN", font="arial 14", width=12, anchor='center', relief='ridge')
label_isbn.grid(row=1, column=2, pady=16)

title_text = StringVar()
entry_title = Entry(window, textvariable=title_text, font='arial 11')
entry_title.grid(row=0, column=1)

author_text = StringVar()
entry_author = Entry(window, textvariable=author_text, font='arial 11')
entry_author.grid(row=0, column=3)

year_text = StringVar()
current_year = datetime.now().year
start_from_year = 2007

year_list = list((range(current_year, start_from_year - 1, -1)))
year_Combo = Combobox(window, textvariable=year_text, values=year_list, font='arial 11', width=18)
year_Combo.grid(row=1, column=1)

isbn_text = StringVar()
entry_isbn = Entry(window, textvariable=isbn_text, font='arial 11')
entry_isbn.grid(row=1, column=3)

books_list = Listbox(window, height=10, width=70, font='arial 10 bold', relief='solid')
books_list.grid(row=3, column=0, rowspan=6, columnspan=4, pady=16)

scroll_bar_yaxes = Scrollbar(window, orient='vertical')
scroll_bar_yaxes.grid(row=3, column=3, rowspan=6)

scroll_bar_xaxes = Scrollbar(window, orient='horizontal')
scroll_bar_xaxes.grid(row=9, column=0, columnspan=5)

books_list.configure(yscrollcommand=scroll_bar_yaxes.set, xscrollcommand=scroll_bar_xaxes)
scroll_bar_yaxes.configure(command=books_list.yview)
scroll_bar_xaxes.configure(command=books_list.xview)

books_list.bind('<<ListboxSelect>>', get_selected_row)

style = Style()
style.configure('TButton', font='arial 12', borderwidth=4)


button_view_all = Button(window, text="View all", width=13, compound='left',
                         style='TButton', command=view_command)
button_view_all.grid(row=10, column=0, padx=16, pady=16)

button_search_entry = Button(window, text="Search entry", width=13, compound='left',
                             style='TButton', command=search_command)
button_search_entry.grid(row=10, column=1, padx=16, pady=16)

button_add_entry = Button(window, text="Add entry", width=13, compound='left',
                          style='TButton', command=add_command)
button_add_entry.grid(row=10, column=2, padx=16, pady=16)

button_update_selected = Button(window, text="Update selected", compound='left', width=13,
                                style='TButton', command=update_command)
button_update_selected.grid(row=11, column=0, padx=16, pady=16)

button_delete_selected = Button(window, text="Delete selected", width=13, compound='left',
                                style='TButton', command=delete_command)
button_delete_selected.grid(row=11, column=1, padx=16, pady=16)

button_clear = Button(window, text="Reset", width=13, compound='left',
                      style='TButton', command=clear_command)
button_clear.grid(row=11, column=2, padx=16, pady=16)

button_close = Button(window, text="Close", width=13, compound='left',
                      style='TButton', command=window.destroy)
button_close.grid(row=12, column=1)

window.mainloop()
