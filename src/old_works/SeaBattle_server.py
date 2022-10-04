import socket
import select
import time
"""
Server accepts only 2 connections, and rejects any others.
If any of those 2 connections is closed or one of the clients wins -- server closes the other and closes itself.
"""

def listening_socket():
    sock1 = socket.socket()
    sock1.setblocking(True)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind(('127.0.0.1', 65432))
    sock1.listen(0)
    return sock1


sock = listening_socket()
LIMIT = 2
conns = {sock}
players_set = 0
turn = 1
while True:
    readable, writable, exceptional = select.select(conns, [], [])
    if sock in readable:  # new connection on the listening socket
        conn, caddr = sock.accept()
        conns.add(conn)
        if len(conns) > LIMIT:  # ">" because "sock" is also in there
            conns.remove(sock)
            sock.close()
            players_set = 1
    else:  # reading from an established connection
        if players_set:
            conn_player1, conn_player2 = readable
            while True:
                buf_player1 = conn_player1.recv(1024)
                if not buf_player1:
                    conn_player1.close()
                    conn_player2.close()
                    exit(0)
                elif (bytes.decode(buf_player1)).split('.')[0] == "End":
                    conn_player2.send(buf_player1)
                    conn_player1.close()
                    conn_player2.close()
                    exit(0)
                else:
                    conn_player2.send(buf_player1)

                buf_player2 = conn_player2.recv(1024)
                if not buf_player2:
                    conn_player1.close()
                    conn_player2.close()
                    exit(0)
                elif (bytes.decode(buf_player2)).split('.')[0] == "End":
                    conn_player1.send(buf_player2)
                    conn_player1.close()
                    conn_player2.close()
                    exit(0)
                else:
                    conn_player1.send(buf_player2)

                if turn:
                    conn_player1.send(str.encode("Your turn"))
                    turn = not turn
                time.sleep(1)
    time.sleep(1)
