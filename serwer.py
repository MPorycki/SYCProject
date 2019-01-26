"""
Co robi serwer:
1. Odbiera dane od robota (COMPLETED, REVISED, TESTED)
2. Zapisuje dane od robota na dysku (COMPLETED, REVISED, TESTED)
3. Generuje ID dla robota (COMPLETED, REVISED, TESTED)
4. Wysyla dla robota potwierdzenie otrzymania danych (COMPLETED, REVISED, TESTED)
5. Zwraca dla klienta info o danym robocie (COMPLETED, REVISED, TESTED)
"""
import copy
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("172.23.1.5", 5002)
sock.bind(address)
stored_data_template = {'ip': '',
                        'data': {'TIMESTAMP': [], 'LIGHT': [], 'TEMP': [], 'PRESSURE': []}}
robot = {}
internal_password = 'e1695548-abb9-4b79-8f24-392a1807666f'
max_robot_id = 0


def generate_id():
    global max_robot_id
    max_robot_id += 1
    return str(max_robot_id)


def reset_id():
    global max_robot_id
    max_robot_id = 0


def handle_request(data):
    request = data[1]
    robot_id = data[0]
    if int(robot_id) > max_robot_id:
        return 'Robot o takim id nie istnieje.'
    if request == '1':
        output = get_light(robot_id)
    elif request == '2':
        output = get_temp(robot_id)
    elif request == '3':
        output = get_pressure(robot_id)
    elif request == '4':
        request_base_return(robot_id)
        output = 'Robot rozpocznie powrot do bazy'
    elif request == '5':
        try:
            request_parameter_change(robot_id, new_interval_val=data[2],
                                     new_mission_len_val=data[3])
            output = 'Wyslano polecenie zmiany parametrow do robota'
        except IndexError:
            output = 'Niewlasciwa liczba parametrow komendy'
    elif request == '6':
        request_data_resend(robot_id)
        output = 'Dane zostaly wyslane ponownie do bazy'
    elif request == internal_password:
        try:
            internal_request = data[2]
        except IndexError:
            output = 'Lack of internal request in the incoming data'
        except Exception:
            output = Exception
        if internal_request == 'data':
            data_to_receive = data[3:]
            receive_data(data_to_receive, robot_id)
            output = '1'
        elif internal_request == 'generate':
            output = str(generate_id())
    elif 'An' in request:
        print("Przeszkoda")
        output = '1'
    else:
        output = 'Wrong input'
    return output


def get_light(requested_robot_id):
    try:
        return '{} : {} Light'.format(robot[requested_robot_id]['data']['TIMESTAMP'][-1],
                                      robot[requested_robot_id]['data']['LIGHT'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def get_temp(requested_robot_id):
    try:
        return '{} : {} Celsius'.format(robot[requested_robot_id]['data']['TIMESTAMP'][-1],
                                        robot[requested_robot_id]['data']['TEMP'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def get_pressure(requested_robot_id):
    try:
        return '{} : {} Pressure'.format(robot[requested_robot_id]['data']['TIMESTAMP'][-1],
                                         robot[requested_robot_id]['data']['PRESSURE'][-1])
    except KeyError:
        return 'Robot with id {} does not exist'.format(requested_robot_id)


def receive_data(received_data, input_robot_id):
    if input_robot_id not in robot.keys() or len(received_data) > 10:
        robot[input_robot_id] = copy.deepcopy(stored_data_template)
        # kiedy pozyskujemy ip???
    for record in received_data:
        if len(record) > 0:
            inputs = record.split(';')
            timestamp = inputs[0] + ' ' + inputs[1]
            light = inputs[2]
            temp = inputs[3]
            pressure = inputs[4]
            robot[input_robot_id]['data']['TIMESTAMP'].append(timestamp)
            robot[input_robot_id]['data']['LIGHT'].append(light)
            robot[input_robot_id]['data']['TEMP'].append(temp)
            robot[input_robot_id]['data']['PRESSURE'].append(pressure)


def request_base_return(robot_id):
    request_message = 'return'
    send_response(request_message, robot[robot_id]['ip'])


def request_parameter_change(robot_id, new_interval_val, new_mission_len_val):
    request_message = 'parameter ' + str(new_interval_val) + ' ' + str(new_mission_len_val)
    send_response(request_message, robot[robot_id]['ip'])


def request_data_resend(robot_id):
    request_message = 'send_all'
    send_response(request_message, robot[robot_id]['ip'])


def send_response(message, recipient_ip):
    sock.sendto(str.encode(message), recipient_ip)


if __name__ == '__main__':
    print('Serwer aktywny. Nasluchuje...')
    while True:
        incoming_message, return_address = sock.recvfrom(1024)
        client_input = incoming_message.decode('utf-8').split(' ')
        print('Received {}'.format(client_input))
        response = handle_request(client_input)
        # DEBUG
        print("Sending {} to {}".format(response, return_address))
        send_response(response, return_address)
