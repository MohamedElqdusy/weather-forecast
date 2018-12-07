from django.test import TestCase
from django.urls import reverse
import mock
import json
from django.http import HttpRequest
from .parse import *
from .views import *
from unittest.mock import Mock, patch


class TestView(TestCase):

    def test_ping(self):
        response = self.client.get('/ping')
        expected = "{\'name\': \'weatherservice\', \'status\': \'ok\', \'version\': \'1.0.0\'}"
        response_str = str(response.json())
        self.assertEquals(response.status_code, 200)
        assert response_str == expected

    @patch('forcast.services.requests.get')
    def test_forecast_by_city(self, mock_get):
        data = "{\"coord\":{\"lon\":145.77,\"lat\":-16.92},\"weather\":[{\"id\":803,\"main\":\"Clouds\",\"description\":\"broken clouds\",\"icon\":\"04n\"}],\"base\":\"cmc stations\",\"main\":{\"temp\":293.25,\"pressure\":1019,\"humidity\":83,\"temp_min\":289.82,\"temp_max\":295.37},\"wind\":{\"speed\":5.1,\"deg\":150},\"clouds\":{\"all\":75},\"rain\":{\"3h\":3},\"dt\":1435658272,\"sys\":{\"type\":1,\"id\":8166,\"message\":0.0166,\"country\":\"AU\",\"sunrise\":1435610796,\"sunset\":1435650870},\"id\":2172797,\"name\":\"Cairns\",\"cod\":200}"
        expected = "{\'temperature\': \'20.1C\', \'pressure\': \'1019 hPa\', \'humidity\': \'83%\', \'clouds\': \'broken clouds\'}"
        
        resp_mock = self.response_mocked(json_data=json.loads(data),content ="application/json")
        mock_get.return_value = resp_mock
        response = forecast_by_city(HttpRequest(),"London")
        result = str(json.loads(response.content))
        
        assert result ==  expected

    @patch('forcast.services.requests.get')
    def test_forecast_by_city_not_found(self, mock_get):
        data = "{\"cod\": \"404\", \"message\": \"city not found\"}"
        resp_mock = self.response_mocked(status= 404,json_data=json.loads(data),content ="application/json")
        mock_get.return_value = resp_mock
        response = forecast_by_city(HttpRequest(),"non")
        result = str(json.loads(response.content))
        
        city_error = country_not_found("non")
        expected = str(json.loads(city_error.content))
        assert response.status_code == 404
        assert result ==  expected

    @patch('forcast.services.requests.get')
    def test_forcast_by_time_invalid_date(self, mock_get):
        data = '{\"cod\":\"200\",\"message\":0.0024,\"cnt\":40,\"list\":[{\"dt\":1544194800,\"main\":{\"temp\":280.75,\"temp_min\":280.247,\"temp_max\":280.75,\"pressure\":1007.92,\"sea_level\":1015.61,\"grnd_level\":1007.92,\"humidity\":95,\"temp_kf\":0.5},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10d\"}],\"clouds\":{\"all\":8},\"wind\":{\"speed\":7.03,\"deg\":265.001},\"rain\":{\"3h\":0.0074999999999994},\"sys\":{\"pod\":\"d\"},\"dt_txt\":\"2018-12-07 15:00:00\"},{\"dt\":1544205600,\"main\":{\"temp\":279.5,\"temp_min\":279.129,\"temp_max\":279.5,\"pressure\":1009.66,\"sea_level\":1017.26,\"grnd_level\":1009.66,\"humidity\":95,\"temp_kf\":0.37},\"weather\":[{\"id\":802,\"main\":\"Clouds\",\"description\":\"scattered clouds\",\"icon\":\"03n\"}],\"clouds\":{\"all\":44},\"wind\":{\"speed\":6.86,\"deg\":255.502},\"rain\":{},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-07 18:00:00\"},{\"dt\":1544216400,\"main\":{\"temp\":280.38,\"temp_min\":280.131,\"temp_max\":280.38,\"pressure\":1009.55,\"sea_level\":1017.25,\"grnd_level\":1009.55,\"humidity\":95,\"temp_kf\":0.25},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":92},\"wind\":{\"speed\":8.6,\"deg\":257.5},\"rain\":{\"3h\":1.295},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-07 21:00:00\"},{\"dt\":1544227200,\"main\":{\"temp\":280.98,\"temp_min\":280.86,\"temp_max\":280.98,\"pressure\":1009.28,\"sea_level\":1016.89,\"grnd_level\":1009.28,\"humidity\":95,\"temp_kf\":0.12},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":88},\"wind\":{\"speed\":8.52,\"deg\":257},\"rain\":{\"3h\":0.004999999999999},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 00:00:00\"},{\"dt\":1544238000,\"main\":{\"temp\":281.584,\"temp_min\":281.584,\"temp_max\":281.584,\"pressure\":1008.92,\"sea_level\":1016.47,\"grnd_level\":1008.92,\"humidity\":90,\"temp_kf\":0},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":92},\"wind\":{\"speed\":9.71,\"deg\":263.5},\"rain\":{\"3h\":0.095000000000001},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 03:00:00\"},{\"dt\":1544248800,\"main\":{\"temp\":282.019,\"temp_min\":282.019,\"temp_max\":282.019,\"pressure\":1009.82,\"sea_level\":1017.39,\"grnd_level\":1009.82,\"humidity\":81,\"temp_kf\":0},\"weather\":[{\"id\":803,\"main\":\"Clouds\",\"description\":\"broken clouds\",\"icon\":\"04n\"}],\"clouds\":{\"all\":64},\"wind\":{\"speed\":9.62,\"deg\":272},\"rain\":{},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 06:00:00\"}],\"city\":{\"id\":2643743,\"name\":\"London\",\"coord\":{\"lat\":51.5073,\"lon\":-0.1277},\"country\":\"GB\",\"population\":1000000}}'
        resp_mock = self.response_mocked(status=400,json_data=json.loads(data),content ="application/json")
        mock_get.return_value = resp_mock
        response = forcast_by_time(HttpRequest(),"London","1444248800,")
        result = str(json.loads(response.content))

        date_error = invalid_date_error()
        expected = str(json.loads(date_error.content))
        assert response.status_code == 400
        assert result ==  expected

    @patch('forcast.services.requests.get')
    def test_forcast_by_time_valid_date(self, mock_get):
        data = '{\"cod\":\"200\",\"message\":0.0024,\"cnt\":40,\"list\":[{\"dt\":1544194800,\"main\":{\"temp\":280.75,\"temp_min\":280.247,\"temp_max\":280.75,\"pressure\":1007.92,\"sea_level\":1015.61,\"grnd_level\":1007.92,\"humidity\":95,\"temp_kf\":0.5},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10d\"}],\"clouds\":{\"all\":8},\"wind\":{\"speed\":7.03,\"deg\":265.001},\"rain\":{\"3h\":0.0074999999999994},\"sys\":{\"pod\":\"d\"},\"dt_txt\":\"2018-12-07 15:00:00\"},{\"dt\":1544205600,\"main\":{\"temp\":279.5,\"temp_min\":279.129,\"temp_max\":279.5,\"pressure\":1009.66,\"sea_level\":1017.26,\"grnd_level\":1009.66,\"humidity\":95,\"temp_kf\":0.37},\"weather\":[{\"id\":802,\"main\":\"Clouds\",\"description\":\"scattered clouds\",\"icon\":\"03n\"}],\"clouds\":{\"all\":44},\"wind\":{\"speed\":6.86,\"deg\":255.502},\"rain\":{},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-07 18:00:00\"},{\"dt\":1544216400,\"main\":{\"temp\":280.38,\"temp_min\":280.131,\"temp_max\":280.38,\"pressure\":1009.55,\"sea_level\":1017.25,\"grnd_level\":1009.55,\"humidity\":95,\"temp_kf\":0.25},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":92},\"wind\":{\"speed\":8.6,\"deg\":257.5},\"rain\":{\"3h\":1.295},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-07 21:00:00\"},{\"dt\":1544227200,\"main\":{\"temp\":280.98,\"temp_min\":280.86,\"temp_max\":280.98,\"pressure\":1009.28,\"sea_level\":1016.89,\"grnd_level\":1009.28,\"humidity\":95,\"temp_kf\":0.12},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":88},\"wind\":{\"speed\":8.52,\"deg\":257},\"rain\":{\"3h\":0.004999999999999},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 00:00:00\"},{\"dt\":1544238000,\"main\":{\"temp\":281.584,\"temp_min\":281.584,\"temp_max\":281.584,\"pressure\":1008.92,\"sea_level\":1016.47,\"grnd_level\":1008.92,\"humidity\":90,\"temp_kf\":0},\"weather\":[{\"id\":500,\"main\":\"Rain\",\"description\":\"light rain\",\"icon\":\"10n\"}],\"clouds\":{\"all\":92},\"wind\":{\"speed\":9.71,\"deg\":263.5},\"rain\":{\"3h\":0.095000000000001},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 03:00:00\"},{\"dt\":1544248800,\"main\":{\"temp\":282.019,\"temp_min\":282.019,\"temp_max\":282.019,\"pressure\":1009.82,\"sea_level\":1017.39,\"grnd_level\":1009.82,\"humidity\":81,\"temp_kf\":0},\"weather\":[{\"id\":803,\"main\":\"Clouds\",\"description\":\"broken clouds\",\"icon\":\"04n\"}],\"clouds\":{\"all\":64},\"wind\":{\"speed\":9.62,\"deg\":272},\"rain\":{},\"sys\":{\"pod\":\"n\"},\"dt_txt\":\"2018-12-08 06:00:00\"}],\"city\":{\"id\":2643743,\"name\":\"London\",\"coord\":{\"lat\":51.5073,\"lon\":-0.1277},\"country\":\"GB\",\"population\":1000000}}'
        resp_mock = self.response_mocked(json_data=json.loads(data),content ="application/json")
        mock_get.return_value = resp_mock
        response = forcast_by_time(HttpRequest(),"London","2018-12-08T06:00:00+00:00")
        result = str(json.loads(response.content))

        weather = "{\"temperature\": \"8.4C\", \"pressure\": \"1008.92 hPa\", \"humidity\": \"90%\", \"clouds\": \"light rain\"}"
        expected = str(json.loads(weather))
        assert result ==  expected

    """
    a test utility for mocking reponse
    """
    def response_mocked (self, status=200, content="CONTENT", json_data=None):  
        resp = mock.Mock()
        resp.raise_for_status = mock.Mock()
        resp.status_code = status
        resp.content = content
        if json_data:
            resp.json = mock.Mock(return_value=json_data)
        return resp