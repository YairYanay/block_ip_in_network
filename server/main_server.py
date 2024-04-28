from network_project.final_project.db.db_func import return_server_status, return_list_of_block_ip, add_packet_info_to_db, recv_ip_send_src_from_db
from network_project.final_project.server.calc_checksum import *

from scapy.all import *
import threading


import socket
MY_ADDRESS = socket.gethostbyname(socket.gethostname())

SUBNET = '255.255.255.0'


def change_to_my_ip_and_fix_packet(packet_data: packet, ip_src: str, ip_dst: str):
    del packet_data[Ether].src, packet_data[Ether].dst
    packet_data[IP].src = ip_src
    packet_data[IP].dst = ip_dst
    if packet_data.haslayer(IP):
        change_ip_checksum(packet_data)
    if packet_data.haslayer(TCP) or packet_data.haslayer(UDP):
        change_tcp_udp_cheksum(packet_data)


def check_ip_doesnt_blocked(packet_data: packet) -> bool:
    ip_block_list = return_list_of_block_ip()
    return ({'IP': packet_data[IP].src} not in ip_block_list) and ({'IP': packet_data[IP].dst} not in ip_block_list)


def send_data(data):
    sendp(data, verbose=False)


def calc_sniff_outside(recv_packet: packet):
    if recv_packet.haslayer(IP) and check_ip_doesnt_blocked(recv_packet):
        print(recv_packet)
        if not check_pc_in_same_network(SUBNET, MY_ADDRESS, recv_packet[IP].src) and recv_packet[IP].dst == MY_ADDRESS:
            pc_send_data_ip = recv_ip_send_src_from_db(recv_packet)
            if pc_send_data_ip:
                change_to_my_ip_and_fix_packet(recv_packet, recv_packet[IP].src, pc_send_data_ip)
                threading.Thread(target=send_data, args=(recv_packet,)).start()


def sniff_outside():
    while return_server_status()['server_status']:
        threading.Thread(target=calc_sniff_outside, args=(sniff(count=1)[0],)).start()


def calc_sniff_inside(send_packet: packet):
    if send_packet.haslayer(IP) and check_ip_doesnt_blocked(send_packet):
        print(send_packet)
        if send_packet[IP].src != MY_ADDRESS and check_pc_in_same_network(SUBNET, MY_ADDRESS, send_packet[IP].src) and not check_pc_in_same_network(SUBNET, MY_ADDRESS, send_packet[IP].dst):
            add_packet_info_to_db(send_packet)
            change_to_my_ip_and_fix_packet(send_packet, MY_ADDRESS, send_packet[IP].dst)
            threading.Thread(target=send_data, args=(send_packet,)).start()


def sniff_inside():
    while return_server_status()['server_status']:
        threading.Thread(target=calc_sniff_inside, args=(sniff(count=1)[0],)).start()
