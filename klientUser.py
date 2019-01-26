import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("172.23.1.5", 5002)
address = ("127.0.0.1", 5002)
sock.bind(address)
possible_requests = {'1': 'getLight', '2': 'getTemperature', '3': 'getPressure', '4': 'baseReturn',
                     '5': 'parameterChange', '6': 'resendData'}


def listen_to_server():
    data, addr = sock.recvfrom(1024)
    server_input = data.decode('utf-8')
    return server_input


if __name__ == '__main__':
    while True:
        var = input(
            "Prosze podac komende do wyslania. \n Forma komend: 'id_robota komenda'. Dostepne "
            "komendy:\n 1 - Ostatnia zapisana wartosc swiatla \n 2 - ostatnia zapisana wartosc "
            "temperatury \n 3 - Ostatnia zapisana wartosc cisnienia \n 4 - rozkaz powrotu do bazy "
            "\n 5 dlugosc_interwalu dlugosc_misji - zmiana parametrow pracy robota (np. 5 1 "
            "100) \n 6 - "
            "ponowne wyslanie wszystkich pomiarow robota do stacji bazowej\n")
        request = var.split(' ')
        if request[1] in possible_requests.keys():
            sock.sendto(str.encode(var), address)
            print('Wyslano polecenie {} do robota o id {}. Oczekiwanie na odpowiedz...'.format(
                possible_requests[request[1]], request[0]))
            response = listen_to_server()
            print(response)
        else:
            print("Niewlasciwa komenda. Prosze wpisac wiadomosc ponownie")
