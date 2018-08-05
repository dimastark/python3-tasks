"""Simple chat application"""
import socket
import sys
import tkinter as tk
from multiprocessing import Manager, Process


HELP = """Simple chat without frills

    Args:
        1: address: ip address to connect (Default localhost)
        2: port: number of port

        if you want start the chat run this without arguments

(c)DimaStark 2015"""


def parse_args(args):
    """Parse args"""
    if args:
        if len(args) == 1:
            if args[0] == '-h' or args[0] == '--help':
                print(HELP)
                sys.exit()
            else:
                addr = '127.0.0.1'
                try:
                    port = int(args[0])
                except ValueError:
                    raise ValueError("Wrong port")
                return addr, port
        elif len(args) == 2:
            addr, port = args
            addr = addr if addr != 'localhost' else '127.0.0.1'
            if addr.count('.') != 3:
                raise ValueError("Wrong address")
            try:
                port = int(port)
            except ValueError:
                raise ValueError("Wrong ip")
            return addr, port
        else:
            raise ValueError("Wrong arguments")


def get_lan_ip():
    """Return your lan ip"""
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with sck as sock:
        sock.connect(("8.8.8.8",80))
        return sock.getsockname()[0]
    

def now_time():
    """Return current time"""
    from datetime import datetime
    cur_time = datetime.now().time()
    return cur_time.strftime("%H:%M")


def set_socket():
    """Setting a socket for a chat

    Returns:
        port_num (str): number of the port
        sock (socket): the ready to work socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    addr = get_lan_ip(), str(sock.getsockname()[1])
    return addr, sock


def send_msg(sock, msg, connected):
    """Send 'to_send' to all client in 'connected'

    Args:
        sock (socket): client's socket
        message (str): message to send
        connected (list): list of clients
    """
    if msg:
        to_send = ('0' + msg).encode('utf-8')
        for client in connected:
            sock.sendto(to_send, client)


def got_msg(sock, msg_box, connected):
    """Wait messages and connect unknown address

    Args:
        sock (socket): client's socket
        msg_box (list): list of messages
        connected (list): list of clients
    """
    while True:
        data, addr = sock.recvfrom(65535)
        enc_data = data.decode('utf-8')
        msg_code, msg = enc_data[0], enc_data[1:]
        if addr not in connected:
            for client in connected:
                to_send = '1' + addr[0] + ' ' + str(addr[1])
                sock.sendto(to_send.encode('utf-8'), client)
            connected.append(addr)
            msg_box.append(addr[0] + ':' + str(addr[1]) + ' connected')
        else:
            if msg_code == '0':
                msg_box.append(str(addr[1]) + ': ' + msg)
            else:
                conn_addr, port = msg.split()
                connected.append(conn_addr)
                msg_box.append(conn_addr + ':' + port + ' connected')


def button_event(sock, entry, text_box, connected):
    """Runs when you press 'send'

    Args:
        sock (socket): client's socket
        entry (tkinter Entry widget): entrance of msg
        text_box (tkinter Text widget): for text from 'entry'
        connected (list): list of clients
    """
    msg = entry.get()
    text_box.config(state='normal')
    if msg:
        entry.delete(0, 'end')
        text_box.insert(tk.END, now_time() + ' I: ' + msg + '\n')
        send_msg(sock, msg, connected)
    text_box.config(state='disabled')


def checker(root, text_box, msg_box):
    """Check for new messages

    Args:
        root (Tk): application
        text_box (tkinter Text widget): for message
        msg_box (list): list of messages
    """
    if msg_box:
        for i in msg_box[::-1]:
            text_box.config(state='normal')
            text_box.insert(tk.END, i + '\n')
            text_box.config(state='disabled')
            msg_box.pop()
    root.after(100, lambda: checker(root, text_box, msg_box))


def main():
    """Entry point"""
    args = parse_args(sys.argv[1:])
    addr, sck = set_socket()
    root = tk.Tk()
    root.resizable(width=False, height=False)
    with Manager() as mng:
        connected = mng.list()
        txt_box = mng.list()
        with sck as sock:
            if args:
                sock.sendto('.'.encode('utf-8'), args)
                connected.append(args)
            ent = tk.Entry(width=60)
            lab = tk.Label(text='Address: ' + addr[0] + ' / port: ' + str(addr[1]))
            txt = tk.Text(width=50, height=15)
            txt.config(state='disabled')
            but = tk.Button(text='Send', command=lambda: button_event(sock, ent, txt, connected))
            ent.bind("<Return>", lambda x: button_event(sock, ent, txt, connected))
            lab.pack()
            txt.pack()
            ent.pack(side='left')
            but.pack(side='right')
            Process(target=got_msg, args=(sock, txt_box, connected)).start()
            root.after(100, lambda: checker(root, txt, txt_box))
            tk.mainloop()


if __name__ == '__main__':
    main()
