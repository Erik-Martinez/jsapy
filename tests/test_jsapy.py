from jsapy.accidents import basic_rate

def test_basic_rate():
    num = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    den = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert basic_rate(10000, 10, 10) == float(10000), "Basic rate with only number works incorrectly!"
    assert basic_rate(num, den, 10) == float(10000), "Basic rate with list works incorrectly!"