from network_project.final_project.pages.pages_func import destroy_widgets

from scapy.all import *
import tkinter as tk
import ipaddress
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def return_server_status() -> dict:
    admin_db = myclient["admin"]
    server_status = admin_db["server_status"]
    return server_status.find_one()


def remove_server_status():
    admin_db = myclient["admin"]
    server_status = admin_db["server_status"]
    try:
        server_status.delete_one(return_server_status())
    except:
        pass


def check_server_status_null() -> int:
    admin_db = myclient["admin"]
    server_status = admin_db["server_status"]
    return server_status.count_documents({})


def change_server_status_in_db():
    admin_db = myclient["admin"]
    server_status = admin_db["server_status"]
    if server_status.count_documents({}) == 0:
        server_status.insert_one({'server_status': False})

    else:
        current_status_doc = return_server_status()
        if current_status_doc:
            new_status = not current_status_doc['server_status']
            server_status.update_one({}, {'$set': {'server_status': new_status}})

        else:
            print("No existing document found in 'server_status' collection.")


def refresh_send_data_in_db(tree):
    mydb = myclient["data_base"]
    list_of_dict_packet_info = mydb["action_send_packet"]
    tree.delete(*tree.get_children())
    for packet_info in list(list_of_dict_packet_info.find({}, {'_id': 0})):
        tree.insert("", '0', values=list(packet_info.values()))


def refresh_ip_block_from_db(listbox: tk.Listbox):
    admin = myclient["admin"]
    list_of_block_ip = admin["block_ip"]

    listbox.delete(0, tk.END)
    for ip in list_of_block_ip.find({}, {'_id': 0}):
        listbox.insert(tk.END, ip['IP'])


def return_list_of_block_ip() -> list:
    admin = myclient["admin"]
    list_of_block_ip = admin["block_ip"]

    return list(list_of_block_ip.find({}, {'_id': 0}))


def add_to_listbox(window: tk.Tk, entry: tk.Entry, listbox: tk.Listbox):
    ipnut_data = entry.get().strip()

    try:
        ipaddress.ip_address(ipnut_data)

        if ipnut_data:
            admin = myclient["admin"]
            list_of_block_ip = admin["block_ip"]
            list_of_block_ip.insert_one({'IP': ipnut_data})

            listbox.insert(tk.END, ipnut_data)
        entry.delete(0, tk.END)

    except:
        label = tk.Label(window, text='error!', font=("Helvetica", 14), fg="red")
        label.place(relx=0.5, rely=0.85, anchor="center")
        label.after(500, lambda: destroy_widgets(label))


def delete_selected_item(window: tk.Tk, listbox: tk.Listbox):
    selected_index = listbox.curselection()

    try:
        if selected_index:
            admin = myclient["admin"]
            list_of_block_ip = admin["block_ip"]
            list_of_block_ip.delete_one({'IP': listbox.get(selected_index)})

            listbox.delete(selected_index)

    except:
        label = tk.Label(window, text='error!', font=("Helvetica", 14), fg="red")
        label.place(relx=0.5, rely=0.85, anchor="center")
        label.after(500, lambda: destroy_widgets(label))


def create_dict_packet_info(packet_data: packet) -> dict:
    return {
        'src': packet_data[IP].src,
        'dst': packet_data[IP].dst,
        'sport': packet_data.getlayer(2).sport if packet_data.haslayer(TCP) or packet_data.haslayer(UDP) else None,
        'dport': packet_data.getlayer(2).dport if packet_data.haslayer(TCP) or packet_data.haslayer(UDP) else None
    }


def add_packet_info_to_db(packet_data: packet):
    dict_packet_info = create_dict_packet_info(packet_data)
    mydb = myclient["data_base"]
    list_of_dict_packet_info = mydb["action_send_packet"]

    if dict_packet_info not in list(list_of_dict_packet_info.find({}, {'_id': 0})):
        list_of_dict_packet_info.insert_one(dict_packet_info)


def recv_ip_send_src_from_db(packet_data: packet) -> str:
    mydb = myclient["data_base"]
    list_of_dict_packet_info = mydb["action_send_packet"]

    for packet_info in list_of_dict_packet_info.find():
        if packet_info_match(packet_data, packet_info):
            return packet_info['src']

    return ""


def packet_info_match(packet_data: packet, packet_info: dict) -> bool:
    if packet_data.haslayer(TCP) or packet_data.haslayer(UDP):
        return (
                packet_data[IP].src == packet_info['dst'] and
                packet_data.getlayer(2).sport == packet_info['dport'] and
                packet_data.getlayer(2).dport == packet_info['sport']
                )
    return packet_data[IP].src == packet_info['dst']
