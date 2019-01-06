"""
Functionalities:
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
"""
import klientRaspberry as klient

test_data = '19-12-2018;15:25:31;1;2;3'


# TODO refactor with Assert
def test_func_1():
    klient.receive_arduino_data(test_data)
    print(klient.stored_data)


def test_func_2_and_3():
    """
    Active server needed
    """
    # test of receiving data and sending to server
    for i in range(11):
        klient.receive_arduino_data(test_data)
    # test of obstacle handling
    klient.handle_obstacle()


def test_func_4():
    klient.handle_obstacle()


def test_func_5():
    print(klient.get_robot_id())


def test_func_7_8_9():
    test_server_input = 'return'
    klient.handle_server_request(test_server_input)
    test_server_input = 'parameters 1 100'
    klient.handle_server_request(test_server_input)


def test_func_10():
    for i in range(15):
        klient.receive_arduino_data(test_data)
    klient.handle_server_request('send_all')


def perform_tests():
    print('Test_func_1:')
    test_func_1()
    print('Test_func_2_3:')
    # Only with client and server both active
    # test_func_2_and_3()
    print('Test_func_4:')
    test_func_4()
    print('Test_func_5:')
    test_func_5()
    print('Test_func_7_8_9:')
    test_func_7_8_9()


if __name__ == '__main__':
    perform_tests()
