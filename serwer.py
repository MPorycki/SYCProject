"""
Co robi serwer:
1. Odbiera dane od robota (COMPLETED, REVISED, TESTED(locally))
2. Zapisuje dane od robota na dysku (COMPLETED, REVISED, TESTED(locally))
3. Generuje ID dla robota (COMPLETED, REVISED, TESTED)
4. Wysyla dla robota potwierdzenie otrzymania danych (COMPLETED, REVISED, TESTED(locally))
5. Zwraca dla klienta info o danym robocie (COMPLETED, REVISED, TESTED(locally)
"""
import copy
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.56.1", 5002)
sock.bind(address)
stored_data_template = {'TIMESTAMP': [], 'LIGHT': [], 'TEMP': [], 'PRESSURE': []}
robot = {}
internal_password = 'e1695548-abb9-4b79-8f24-392a1807666f'
requests = {'1': 'LIGHT', '2': 'TEMP', '3': 'PRESSURE'}
max_robot_id = 0


def generate_id():
    global max_robot_id
    max_robot_id += 1
    return str(max_robot_id)


def reset_id():
    global max_robot_id
    max_robot_id = 0


def get_light(requested_robot_id):
    try:
        return '{} : {} Light'.format(robot[requested_robot_id]['TIMESTAMP'][-1],
                                      robot[requested_robot_id]['LIGHT'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def get_temp(requested_robot_id):
    try:
        return '{} : {} Celsius'.format(robot[requested_robot_id]['TIMESTAMP'][-1],
                                        robot[requested_robot_id]['TEMP'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def get_pressure(requested_robot_id):
    try:
        return '{} : {} Pressure'.format(robot[requested_robot_id]['TIMESTAMP'][-1],
                                         robot[requested_robot_id]['PRESSURE'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def receive_data(received_data, input_robot_id):
    if input_robot_id not in robot.keys():
        robot[input_robot_id] = copy.deepcopy(stored_data_template)
    for record in received_data:
        inputs = record.split(';')
        timestamp = inputs[0] + ' ' + inputs[1]
        light = inputs[2]
        temp = inputs[3]
        pressure = inputs[4]
        robot[input_robot_id]['TIMESTAMP'].append(timestamp)
        robot[input_robot_id]['LIGHT'].append(light)
        robot[input_robot_id]['TEMP'].append(temp)
        robot[input_robot_id]['PRESSURE'].append(pressure)


def send_response(message, recipient_ip):
    sock.sendto(str.encode(message), recipient_ip)


if __name__ == '__main__':
    print('Serwer aktywny. Nasluchuje...')
    while True:
        data, return_address = sock.recvfrom(512)
        client_input = data.decode('utf-8').split(' ')
        print('Received {}'.format(client_input))
        request = client_input[1]
        robot_id = client_input[0]
        # TODO: refactor it using getAttr?
        if request == '1':
            output = get_light(robot_id)
        elif request == '2':
            output = get_temp(robot_id)
        elif request == '3':
            output = get_pressure(robot_id)
        elif request == internal_password:
            try:
                internal_request = client_input[2]
            except IndexError:
                output = 'Lack of internal request in the incoming data'
            except Exception:
                output = 'Unknown Error'
            if internal_request == 'data':
                data = client_input[3:]
                receive_data(data, robot_id)
                output = '1'
            elif internal_request == 'generate':
                output = str(generate_id())

        else:
            output = 'Wrong input'
        # DEBUG
        print("Sending {} to {}".format(output, return_address))
        send_response(output, return_address)
