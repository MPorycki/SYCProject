import klientRaspberry as klient


def test_func_1():
    test_data = '19-12-2018;15:25:31;1;2;3'
    klient.receive_arduino_data(test_data)
    print(klient.stored_data)
    klient.reset_data()
    print(klient.stored_data)


def test_func_2_and_3():
    """
    Active server needed
    """
    test_data = '19-12-2018;15:25:31;1;2;3'
    for i in range(10):
        klient.receive_arduino_data(test_data)
    print(klient.stored_data)


def test_func_4():
    klient.handle_obstacle()


def test_func_5():
    return klient.get_robot_id()


def perform_tests():
    print('Test_func_1:\n')
    test_func_1()
    print('Test_func_4:\n')
    test_func_4()
    print('Test_func_5:\n')
    test_func_5()


if __name__ == '__main__':
    perform_tests()
