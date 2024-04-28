from pages.pages_func import *
from db.db_func import change_server_status_in_db, remove_server_status


import time
import threading
import tkinter as tk


threads = []


def kill_threads():
    global threads
    change_server_status_in_db()
    for thread in threads:
        thread.join()
        print('shut down thread')
    threads = []
    time.sleep(0.1)


def change_server_status(btn_server_stat: tk.Button, click=False):
    server_status_click = return_server_status()['server_status']
    if not click:
        server_status_click = not server_status_click
    if server_status_click:
        btn_server_stat.config(text='OFF', bg='red')  # Change text to "OFF" and background color to red
        if click:
            kill_threads()

    else:
        btn_server_stat.config(text='ON', bg='green')  # Change text to "ON" and background color to green
        if click:
            change_server_status_in_db()
            from server import main_server
            t = threading.Thread(target=main_server.sniff_inside)
            threads.append(t)
            t.start()
            print('start sniff inside thread')
            t = threading.Thread(target=main_server.sniff_outside)
            threads.append(t)
            t.start()
            print('start sniff outside thread')


def create_main_menu(window: tk.Tk):
    if check_server_status_null() == 0:  #create server status in db
        change_server_status_in_db()

    window.title("Server Management")

    # Add 'MENU' label at the top center
    menu_label_text = tk.Label(window, text="MENU", font=("Helvetica", 20))
    menu_label_text.place(relx=0.5, rely=0.05, anchor="center")

    # Define button dimensions for the main window
    button_width = 15
    button_height = 2

    # Calculate button positioning
    x_coord = 500
    y_coord_start = 300
    y_spacing = 100

    on_off_server_text = tk.Label(window, text='server stat:', font=('Arial', 24))
    on_off_server_text.place(x=x_coord - 175, y=y_coord_start + 3)

    # Create buttons with fixed size using place() method
    btn_server_stat = tk.Button(window, text="", command=lambda: (change_server_status(btn_server_stat, True)), width=button_width, height=button_height, font=("Helvetica", 14))
    btn_server_stat.place(x=x_coord, y=y_coord_start)
    change_server_status(btn_server_stat)

    btn_see_data = tk.Button(window, text="See Data Sent", command=lambda: (destroy_widgets(menu_label_text, on_off_server_text, btn_server_stat, btn_see_data, btn_block_ip, btn_exit), data_send_info_window(window)), width=button_width, height=button_height, font=("Helvetica", 14))
    btn_see_data.place(x=x_coord, y=y_coord_start + y_spacing)

    btn_block_ip = tk.Button(window, text="Block IP", command=lambda: (destroy_widgets(menu_label_text, on_off_server_text, btn_server_stat, btn_see_data, btn_block_ip, btn_exit), create_block_ip_window(window)), width=button_width, height=button_height, font=("Helvetica", 14))
    btn_block_ip.place(x=x_coord, y=y_coord_start + 2 * y_spacing)

    btn_exit = tk.Button(window, text="Exit", command=lambda: (kill_threads(), remove_server_status(), exit_app(window)), width=button_width, height=button_height, font=("Helvetica", 14))
    btn_exit.place(x=x_coord, y=y_coord_start + 3 * y_spacing)


def main():
    screen = tk.Tk()

    window_width = 1200
    window_height = 720

    screen.geometry(f"{window_width}x{window_height}")  # Width x Height
    create_main_menu(screen)

    screen.mainloop()


if __name__ == '__main__':
    main()
