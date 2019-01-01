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
7. Wykonywanie polecen z centrali
8. Wyslanie do arduino komendy powrot
9. Wyslanie do arduino info o zmianie charakterystyki pomiarow
10. Wyslanie wszystkich pomiarow ponownie
26.12 todo:
1-5 completed, revised, tests prepared
"""
import datetime
import serial
import socket


internal_password = 'e1695548-abb9-4b79-8f24-392a1807666f'
stored_data = []
#ser = serial.Serial('/dev/ttyACM0', 9600) # TODO fix AttributeError: module 'serial' has no attribute 'Serial'
robot_id = None
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.56.1", 5002)
sock.bind(address)


def __init__():
    global robot_id
    robot_id = generate_id()
    print('Robot id is {}'.format(robot_id))


def listen_to_server():
    data, addr = sock.recvfrom(1024)
    server_input = data.decode('utf-8')
    return server_input


def generate_id():
    server_connect_and_send("e1695548-abb9-4b79-8f24-392a1807666f generate ")
    received_id = listen_to_server()
    return received_id


def get_robot_id():
    global robot_id
    if robot_id is None:
        return None
    return robot_id


def reset_data():
    # TODO how much data can I store on the robot (additional task no.10)
    global stored_data
    print("Data sent and reset")
    stored_data = []


def receive_arduino_data(input_data):
    stored_data.append(input_data)
    if len(stored_data) >= 10:
        send_data()


def server_connect_and_send(data_to_send):
    global address, robot_id
    if robot_id is not None:
        robo_id = get_robot_id()
        data_to_send = robo_id + ' ' + data_to_send
    else:
        data_to_send = "None " + data_to_send
    sock.sendto(str.encode(data_to_send), address)


def send_data():
    data = 'e1695548-abb9-4b79-8f24-392a1807666f data '
    for element in stored_data:
        data += element + ' '
    server_connect_and_send(data)
    response = listen_to_server()
    if response != '1':
        send_data()
    else:
        reset_data()


def handle_obstacle():
    timestamp = str(datetime.datetime.now())
    message = 'An obstacle has occurred at {}'.format(timestamp)
    server_connect_and_send(message)


if __name__ == '__main__':
    while True:
        #read_serial = ser.readline()
        print("Data read")
        #input = read_serial.split(';')
        input = ''
        if input[0] == 'przeszkoda':
            handle_obstacle()
        else:
            pass
            #receive_arduino_data(read_serial)
