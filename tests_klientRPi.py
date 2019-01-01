import klientRaspberry as klient

test_data = '19-12-2018;15:25:31;1;2;3'


def test_func_1():
    klient.receive_arduino_data(test_data)
    print(klient.stored_data)
    klient.reset_data()
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


def perform_tests():
    print('Test_func_1:\n')
    test_func_1()
    print('Test_func_4:\n')
    test_func_4()
    print('Test_func_5:\n')
    test_func_5()
    print('Test_func_2_3:\n')
    test_func_2_and_3()


if __name__ == '__main__':
    perform_tests()
