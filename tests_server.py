import serwer


def test_func_3():
    print(serwer.generate_id())
    print(serwer.generate_id())
    print(serwer.max_robot_id)
    serwer.reset_id()
    print(serwer.max_robot_id)


def test_func_5():
    id = serwer.generate_id()
    serwer.receive_data(['19-12-2018;15:25:31;1;2;3', '19-12-2018;15:25:31;1;2;3', '19-12-2018;15:25:31;1;2;3'], '1')
    print(serwer.get_light(id))
    print(serwer.get_pressure(id))
    print(serwer.get_temp(id))


def perform_tests():
    print('Test_func_3:')
    test_func_3()
    print('Test_func_5')
    test_func_5()


if __name__ == '__main__':
    perform_tests()
