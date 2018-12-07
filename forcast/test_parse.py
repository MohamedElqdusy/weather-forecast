from unittest import TestCase
from .parse import *

class TestParse(TestCase):
    def test_parse_humidity(self):
        #normal
        h = parse_humidity(52)
        assert h == '52%'

        # empty string
        h2 = parse_humidity('')
        assert h2 == '%'

    def test_parse_temperature(self):
        #big float point
        t = parse_temperature(284.0246325541)
        assert t == '10.9C'
        #Integer
        t2 = parse_temperature(658)
        assert t2 == '384.9C'

    def test_parse_pressure(self):
        #normal
        p = parse_pressure(1019.36)
        assert p == '1019.36 hPa'

        #  empty string
        p2 = parse_pressure('')
        assert p2 == ' hPa'
    
    def test_parse_iso8601_to_timestamp(self):
        t = parse_iso8601_to_timestamp("2018-12-06T09:00:00+00:00")
        assert t == '1544086800'

        # without the clock
        t2 = parse_iso8601_to_timestamp("2018-12-06T09")
        assert t2 == '1544086800'

        # without the day
        t3 = parse_iso8601_to_timestamp("2018-12")
        assert t3 == '1543622400'

        # wrong format
        self.assertRaises(Exception,parse_iso8601_to_timestamp,"26018-125")
    
    def test_is_valid_date(self):
        # wrong iso8601 format
        b = is_valid_date("666","1544065514")
        assert b == False

        # less than 3 hours diff
        b2 = is_valid_date("2018-12-06T06:00:00+00:00","1544065514")
        assert b2 == False

        # more than 3 hours diff
        b3 = is_valid_date("2018-12-07T06:00:00+00:00","1544065514")
        assert b3 == False

        # 3 hours diff
        b4 = is_valid_date("2018-12-06T06:00:00+00:00","1544065200")
        assert b4 == True

    def test_time_diff(self):
        diff = time_diff(1543622400,1543622400)
        assert diff == 0

        diff2 = time_diff(1544076000,1544065200)
        assert diff2 == 3

        diff3 = time_diff(1544076000,1544065514)
        assert diff3 == 2

    def test_parse_weather_data(slef):
        data = "{\"coord\": {\"lon\": -0.13, \"lat\": 51.51}, \"weather\": [{\"id\": 300, \"main\": \"Drizzle\", \"description\": \"light intensity drizzle\",\"icon\":\"09d\"}], \"base\": \"stations\", \"main\": {\"temp\": 285.15, \"pressure\": 1014, \"humidity\": 93, \"temp_min\": 284.15, \"temp_max\": 286.15}, \"visibility\": 10000, \"wind\": {\"speed\": 6.7, \"deg\": 210}, \"clouds\": {\"all\": 20}, \"dt\": 1544106000, \"sys\": {\"type\": 1, \"id\": 1412, \"message\": 0.0046, \"country\": \"GB\", \"sunrise\": 1544082661, \"sunset\": 1544111540}, \"id\": 2643743, \"name\": \"London\", \"cod\": 200}"
        expected = "{\"temperature\": \"12.0C\", \"pressure\": \"1014 hPa\", \"humidity\": \"93%\", \"clouds\": \"light intensity drizzle\"}"
        json_data = json.loads(data)
        parsed = parse_weather_data(json_data)
        assert parsed == expected



