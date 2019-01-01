import socket
from klientRaspberry import listen_to_server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.56.1", 5002)
possible_requests = ['1', '2', '3', '4']


if __name__ == '__main__':
    while True:
        var = input("Prosze podac wiadomosc do wyslania\n")
        # TODO implement the correct format of data input + guidelines for user
        if var in possible_requests:
            if var != '4':
                sock.sendto(str.encode(var), address)
                print('Wyslano na adres {}'.format(address))
                response = listen_to_server()
            else:
                exit(0)
        else:
            print("Niewlasciwa komenda. Prosze wpisac wiadomosc ponownie")
