import serwer
import klientRaspberry

test_data_entry = '19-12-2018;15:25:31;1;2;3'


def test_func_3():
    print(serwer.generate_id())
    print(serwer.generate_id())
    print(serwer.max_robot_id)
    serwer.reset_id()
    print(serwer.max_robot_id)


def test_func_5():
    id = serwer.generate_id()
    serwer.receive_data([test_data_entry, test_data_entry, test_data_entry], '1')
    print(serwer.get_light(id))
    print(serwer.get_pressure(id))
    print(serwer.get_temp(id))


def test_func_1_2():
    klient = klientRaspberry()
    # test of receiving data and sending to server
    for i in range(11):
        klient.receive_arduino_data(test_data_entry)
    # test of obstacle handling
    klient.handle_obstacle()


def perform_tests():
    print('Test_func_3:')
    test_func_3()
    print('Test_func_5')
    test_func_5()


if __name__ == '__main__':
    perform_tests()
