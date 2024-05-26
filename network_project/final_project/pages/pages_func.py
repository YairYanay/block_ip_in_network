from network_project.final_project.db.db_func import *
from tkinter import ttk, Tk


def destroy_widgets(*args: Tk):
    for labal in args:
        labal.destroy()


def exit_app(root: Tk):
    root.destroy()


def data_send_info_window(window: Tk):
    data_send_window_text = tk.Label(window, text="data send", font=("Helvetica", 20))
    data_send_window_text.place(relx=0.5, rely=0.05, anchor="center")

    # Create Table for send data
    table = ttk.Treeview(window, columns=("Column1", "Column2", "Column3", "Column4"), show="headings")

    # Define column headings and set column width
    table.heading("Column1", text="src IP")
    table.heading("Column2", text="dst IP")
    table.heading("Column3", text="src PORT")
    table.heading("Column4", text="dst PORT")

    table.column("Column1", width=200)
    table.column("Column2", width=200)
    table.column("Column3", width=200)
    table.column("Column4", width=200)

    table.place(relx=0.5, rely=0.52, height=450, anchor="center")
    refresh_send_data_in_db(table)

    refresh_send_db_btn = tk.Button(window, text="Refresh", command=lambda: (refresh_send_data_in_db(table)), width=15, height=2, font=("Helvetica", 12))
    refresh_send_db_btn.place(relx=0.9, rely=0.9, anchor="center")

    text_of_function_send_db = tk.Label(window, text="List Of Send Data In Network", font=("Helvetica", 14))
    text_of_function_send_db.place(relx=0.5, rely=0.15, anchor="center")

    import network_project.final_project.main as main
    btn_exit_send_data = tk.Button(window, text="Exit", command=lambda: (
    destroy_widgets(data_send_window_text, table, refresh_send_db_btn, text_of_function_send_db, btn_exit_send_data), main.create_main_menu(window)), width=15,
                                   height=2, font=("Helvetica", 14))
    btn_exit_send_data.place(relx=0.1, rely=0.9, anchor="center")


def create_block_ip_window(window: Tk):
    block_ip_window_text = tk.Label(window, text="BLOCK IP", font=("Helvetica", 20))
    block_ip_window_text.place(relx=0.5, rely=0.05, anchor="center")

    # Create an entry widget for text input
    entry = tk.Entry(window, font=("Helvetica", 14), width=48)
    entry.place(relx=0.49, rely=0.25, anchor="center")

    # Create a listbox widget to display items
    listbox = tk.Listbox(window, font=("Helvetica", 14), width=60, height=15)
    listbox.place(relx=0.5, rely=0.55, anchor="center")
    refresh_ip_block_from_db(listbox)

    add_to_list_btn = tk.Button(window, text="Add", command=lambda: add_to_listbox(window, entry, listbox), font=("Helvetica", 14))
    add_to_list_btn.place(relx=0.24, rely=0.25, anchor="center")

    # Create a "Delete" button to delete selected item from the listbox
    delete_ip_input_btn = tk.Button(window, text="Delete", command=lambda: delete_selected_item(window, listbox), font=("Helvetica", 14))
    delete_ip_input_btn.place(relx=0.75, rely=0.25, anchor="center")

    refresh_ip_block_db_btn = tk.Button(window, text="Refresh", command=lambda: (refresh_ip_block_from_db(listbox)), width=15, height=2, font=("Helvetica", 12))
    refresh_ip_block_db_btn.place(relx=0.9, rely=0.9, anchor="center")

    text_of_function_block_ip = tk.Label(window, text="List Of Block IP In Network", font=("Helvetica", 14))
    text_of_function_block_ip.place(relx=0.5, rely=0.15, anchor="center")

    import network_project.final_project.main as main
    btn_exit_ip = tk.Button(window, text="Exit", command=lambda: (
    destroy_widgets(block_ip_window_text, entry, listbox, add_to_list_btn, delete_ip_input_btn, refresh_ip_block_db_btn, text_of_function_block_ip, btn_exit_ip), main.create_main_menu(window)), width=15,
                            height=2, font=("Helvetica", 14))
    btn_exit_ip.place(relx=0.1, rely=0.9, anchor="center")
