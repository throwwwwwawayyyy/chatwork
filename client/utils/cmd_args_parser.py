import sys

from constants.communication import HOST_ADDR, PORT_NUM

def from_args() -> tuple[str, int]:
    if(len(sys.argv) < 3):
        host_addr = HOST_ADDR
        port_num = PORT_NUM
    else:
        host_addr = sys.argv[1]
        port_num = int(sys.argv[2])

    return host_addr, port_num