from scapy import all as scapy

from bytex import Structure, Endianes
from bytex.types import U3, U4, U16, U32, Flag


class TCPFlags(Structure):
    cwr: Flag
    ece: Flag
    urg: Flag
    ack: Flag
    psh: Flag
    rst: Flag
    syn: Flag
    fin: Flag


class TCP(Structure):
    source_port: U16
    dest_port: U16
    sequence_number: U32
    ack_number: U32

    data_offset: U4
    reserved: U3
    ns_flag: Flag

    flags: TCPFlags

    window_size: U16
    checksum: U16
    urgent_pointer: U16


def tcp_packet_handler(packet: scapy.Packet) -> None:
    data = packet[scapy.TCP].build()  # type: ignore

    tcp = TCP.parse(data, endianes=Endianes.BIG)
    scapy_tcp = packet[scapy.TCP]  # type: ignore

    assert tcp.source_port == scapy_tcp.sport
    assert tcp.dest_port == scapy_tcp.dport
    assert tcp.sequence_number == scapy_tcp.seq
    assert tcp.ack_number == scapy_tcp.ack

    assert tcp.flags.cwr == scapy_tcp.flags.C
    assert tcp.flags.ece == scapy_tcp.flags.E
    assert tcp.flags.urg == scapy_tcp.flags.U
    assert tcp.flags.ack == scapy_tcp.flags.A
    assert tcp.flags.psh == scapy_tcp.flags.P
    assert tcp.flags.rst == scapy_tcp.flags.R
    assert tcp.flags.syn == scapy_tcp.flags.S
    assert tcp.flags.fin == scapy_tcp.flags.F

    assert tcp.window_size == scapy_tcp.window
    assert tcp.checksum == scapy_tcp.chksum
    assert tcp.urgent_pointer == scapy_tcp.urgptr

    print(tcp)


def main() -> None:
    scapy.sniff(filter="tcp", prn=tcp_packet_handler, store=0)


if __name__ == "__main__":
    main()
