import sys

from constants.communication import HOST_ADDR, PORT_NUM, DEBUG_DEFAULT
from constants.logic import DEBUG_KEYWORD

def from_args() -> tuple[str, int, bool]:
    if(len(sys.argv) < 3):
        host_addr = HOST_ADDR
        port_num = PORT_NUM
        debug_flag = DEBUG_DEFAULT
    else:
        host_addr = sys.argv[1]
        port_num = int(sys.argv[2])
        debug_flag = (sys.argv[3] == DEBUG_KEYWORD)

    return host_addr, port_num, debug_flag