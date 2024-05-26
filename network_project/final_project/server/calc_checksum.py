import binascii
from scapy.all import *


def check_pc_in_same_network(subnet_layer: str, pc_1_addr: str, pc_2_addr: str) -> bool:
    assert isinstance(subnet_layer, str) and '.' in subnet_layer, 'subnet_layer must be a string'
    assert isinstance(pc_1_addr, str) and '.' in pc_1_addr, 'MY_PC_ADDR must be a string'
    assert isinstance(pc_2_addr, str) and '.' in pc_2_addr, 'SEC_PC_ADDR must be a string'

    subnet_mask = [int(x) for x in subnet_layer.split('.')]
    pc_1_addr = [int(x) for x in pc_1_addr.split('.')]
    pc_2_addr = [int(x) for x in pc_2_addr.split('.')]

    # Calculate the network address for each IP address using Subnet mask
    pc_1_addr = [pc_1_addr[i] & subnet_mask[i] for i in range(4)]
    pc_2_addr = [pc_2_addr[i] & subnet_mask[i] for i in range(4)]

    return pc_1_addr == pc_2_addr


def calculate_checksum(data_calc_chksum: str) -> int:
    sum = 0
    if len(data_calc_chksum) % 4 != 0:
        data_calc_chksum += '00'

    for i in range(0, len(data_calc_chksum), 4):
        sum += int(data_calc_chksum[i: i+4], 16)

    while sum > int('FFFF', 16):
        sum = hex(sum)
        sum = int(sum[-4:], 16) + int(sum[len('0x'):-4], 16)

    return int('FFFF', 16) - sum


def calculate_ip_to_4_bytes(ip_addr: str) -> str:
    ip_addr = [hex(int(i))[len('0x'):].zfill(2) for i in ip_addr.split('.')]
    return ''.join(ip_addr)


def change_tcp_udp_cheksum(packet_data: packet):
    packet_data.getlayer(2).chksum = 0
    protocol_data = binascii.hexlify(bytes(packet_data.getlayer(2))).decode()
    protocol_len_2_bytes = hex(len(protocol_data) // 2)[len('0x'):].zfill(4)
    # Add all data to one variable and protocol calculate checksum
    calc_protocol_checksum_data = (calculate_ip_to_4_bytes(str(packet_data[IP].src)) + calculate_ip_to_4_bytes(str(packet_data[IP].dst)) +
                                   '00' + str(hex(packet_data[IP].proto)[len('0x'):].zfill(2)) + protocol_len_2_bytes + protocol_data)
    packet_data.getlayer(2).chksum = calculate_checksum(calc_protocol_checksum_data)


def change_ip_checksum(packet_data: packet):
    packet_data[IP].chksum = 0
    packet_data[IP].chksum = calculate_checksum(str(binascii.hexlify(bytes(packet_data[IP])[:len(bytes(packet_data[IP])) - len(bytes(packet_data.getlayer(2)))]))[len("b'"):-1])
