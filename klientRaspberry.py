"""
Co robi klientRaspberry:
1. Odbiera dane z Arduino (COMPLETED, REVISED, TESTED)
2. Przechowuje dane az do momentu, w ktorym ma je wyslac (COMPLETED, REVISED)
3. Wysyla dane do serwera (COMPLETED, REVISED)
4. Odbiera dane o przeszkodzie i natychmiast wysyla je do serwera (COMPLETED, REVISED)
5. Wygenerowac sobie ID (COMPLETED, REVISED)
6. Wyslanie info do Arduino ze koniec misji i wracamy (stop pomiary)
Dodatkowe
6. Nasluchiwanie polecen z centrali
7. Wykonywanie polecen z centrali (COMPLETED, REVISED, TESTED)
8. Wyslanie do arduino komendy powrot (COMPLETED, REVISED, TESTED)
9. Wyslanie do arduino info o zmianie charakterystyki pomiarow (COMPLETED, REVISED, TESTED)
10. Wyslanie wszystkich pomiarow ponownie (COMPLETED, RESVISED)
26.12 todo:
1-5 completed, revised, tests prepared
"""
import datetime
import socket

import serial

internal_password = 'e1695548-abb9-4b79-8f24-392a1807666f'
stored_data = []
ser = serial.Serial('/dev/ttyACM0', 9600)
robot_id = None
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("192.168.8.110", 5002)
address = ("192.168.8.110", 5002)
sock.bind(address)
sock.settimeout(1)


def listen_to_server():
    try:
        data, addr = sock.recvfrom(1024)
        server_input = data.decode('utf-8')
        return server_input
    except socket.timeout:
        print('Nasluchiwanie przerwane')
        return None



def generate_id():
    server_connect_and_send("e1695548-abb9-4b79-8f24-392a1807666f generate ")
    received_id = listen_to_server()
    return received_id


def get_robot_id():
    global robot_id
    if robot_id is None:
        return None
    return robot_id


def receive_arduino_data(input_data):
    stored_data.append(input_data)
    if len(stored_data) % 10 == 0:
        send_data(send_all_data=False)


def server_connect_and_send(data_to_send):
    global address, robot_id
    if robot_id is not None:
        robo_id = get_robot_id()
        data_to_send = robo_id + ' ' + data_to_send
    else:
        data_to_send = "None " + data_to_send
    print("Sending data")
    sock.sendto(str.encode(data_to_send), server_address)


def send_data(send_all_data: bool):
    data = 'e1695548-abb9-4b79-8f24-392a1807666f data '
    if send_all_data:
        to_send = stored_data
    else:
        to_send = stored_data[-10:]
    for element in to_send:
        data += element + ' '
    server_connect_and_send(data)
    response = listen_to_server()
    print("Otrzymalem {}".format(response))
    if response != '1':
        send_data(send_all_data=False)


def send_request_to_arduino(message):
    # DEBUG without Arduino present:
    print('Wyslalem do Arduino {}'.format(message))
    ser.write(message)


def handle_server_request(server_command):
    # form of data sent from server: parameters interval_value missionLength_value
    received_input = server_command.split(' ')
    if server_command == 'return':
        send_request_to_arduino('2')
        server_connect_and_send('Returning-to-base')
    elif server_command == 'send_all':
        send_data(send_all_data=True)
    elif received_input[0] == 'parameters':
            send_request_to_arduino('1')
            send_request_to_arduino(received_input[1])
            send_request_to_arduino(received_input[2])
            server_connect_and_send(
                'Interval change to {} and mission length to {}'.format(received_input[1],
                                                                        received_input[2]))


def handle_obstacle():
    timestamp = str(datetime.datetime.now()).replace(' ', '-')
    message = 'An-obstacle-has-occurred-at-{}'.format(timestamp)
    server_connect_and_send(message)


robot_id = generate_id()
if __name__ == '__main__':
    while True:
        if ser.in_waiting:
            read_serial = ser.readline()
        print("Arduino data read")
        arduino_input = read_serial.split(';')
        arduino_input = ''
        # jak nie czekac na to w nieskonczonosc?
        server_input = listen_to_server()
        if server_input is not None:
            handle_server_request(server_input)
        if arduino_input[0] == 'przeszkoda':
            handle_obstacle()
        elif arduino_input is not None and arduino_input[0] != 'koniec':
            receive_arduino_data(read_serial)
