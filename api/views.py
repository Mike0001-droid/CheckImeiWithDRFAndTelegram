import os
import requests
from rest_framework.decorators import action
import logging
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from decouple import config


logging.basicConfig(level=logging.INFO)
IMEICHECK_API_KEY=config('IMEICHECK_API_KEY')


class CheckImeiViewSet(ViewSet):
    @action(
        detail=False,
        methods=['get'],
        url_path='check_imei/(?P<imei>[a-zA-Z0-9_]+)',
        url_name='by-check_imei',
    )
    def check_imei(self, request, imei):
        
        if request.user.is_anonymous:
            return Response(
                {
                    "detail": "error", 
                    "result": "Пользователь не авторизован, войдите в систему, либо зарегистрируйтесь"
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        if len(imei) not in {14, 15} or not imei.isdigit():
            return Response(
                {
                    "detail": "error", 
                    "result": "Неверный формат IMEI. Пожалуйста, отправьте от 8 до 15 цифр."
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        url = "https://api.imeicheck.net/v1/checks"
        headers = {
            "Authorization": f"Bearer {IMEICHECK_API_KEY}",
            "Content-Type": "application/json",
            "Accept-Language": "en"
        }
        body = {
            "deviceId": imei,
            "serviceId": config('SERVICE_ID'),
            "type": "sandbox"
        }

        logging.info(
            f"Отправка запроса: URL={url}, Headers={headers}, Body={body}"
        )

        try:
            response = requests.post(url, headers=headers, json=body, timeout=10)
            logging.info(
                f"Получен ответ: Status Code={response.status_code}, Body={response.text}"
            )
            if response.status_code == 201:
                result = response.json()
                properties = result.get('properties', {})
                device_name = properties.get('deviceName', 'Неизвестное устройство')
                imei = properties.get('imei', 'Неизвестен')
                model_desc = properties.get('modelDesc', 'Неизвестная модель')
                purchase_country = properties.get('purchaseCountry', 'Неизвестная страна')
                sim_lock = "Да" if properties.get('simLock') else "Нет"
                image_url = properties.get('image', '')

                formatted_result = {
                    "Название устройства": device_name,
                    "Модель устройства": model_desc,
                    "IMEI": imei,
                    "Описание модели": model_desc,
                    "Страна покупки": purchase_country,
                    "Блокировка SIM": sim_lock,
                    "Изображение устройства": image_url
                }
                
                return Response(
                    {
                        "detail": "sucess", 
                        "result": formatted_result
                    }, status=status.HTTP_200_OK
                )
            
            elif response.status_code == 422:
                error_details = response.json()
                logging.error(f"Ошибка валидации данных: {error_details}")
                errors = error_details.get("errors", {})
                if "deviceId" in errors:
                    return Response(
                        {
                            "detail": "error", 
                            "result": f"Недопустимый IMEI: {errors['deviceId'][0]}"
                        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )
                else:
                    return Response(
                        {
                            "detail": "error", 
                            "result": f"{error_details.get('message', 'Неизвестная ошибка')}"
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            return Response(
                {
                    "detail": "error", 
                    "result": f"HTTP ошибка: {http_err}"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {
                    "detail": "error", 
                    "result": f"Ошибка при проверке IMEI: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST
            )
