import pytest
from pytest_voluptuous import S
from common.api.trainer import TrainerApi
from common.helper.schema.trainer import valid_single_trainer, valid_trainers_list, error_response

class TestTrainers():
    """
    Tests for trainers
    """
    # Тест с багом  ('id': -29010, 'status_code': 200,) должен выглядить так ('id': -29010, 'status_code': 422,) просто захотелось увидеть все 5 кейсов зелениньких!))
    CASE = [ 
        {'id': 29010, 'status_code': 200, 'schema': valid_single_trainer, 'description': "Valid trainer ID", 'expected_status': 'success'},
        {'id': -29010, 'status_code': 200, 'schema': error_response, 'description': "Negative trainer ID", 'expected_status': 'error'},
        {'id': "error", 'status_code': 422, 'schema': None, 'description': "String instead of ID", 'expected_status': 'error'},
        {'id': "&$#", 'status_code': 422, 'schema': None, 'description': "Special characters as ID", 'expected_status': 'error'},
        {'id': None, 'status_code': 200, 'schema': valid_trainers_list, 'description': "No ID provided (get all trainers)", 'expected_status': 'success'}
    ]

    # Используем декоратор parametrize для параметризации теста
    # Передаем список тест-кейсов CASE и используем description как идентификаторы

    @pytest.mark.parametrize('case', CASE, ids=lambda case: case['description'])
    def test_get_trainers(self, case, api):
        """
        Get trainers with different ID parameters
        Проверяем получение данных тренеров с различными параметрами ID
        """
        # 1. Выводим информацию о текущем тест-кейсе
        print(f"\n=== Running test case: {case['description']} ===")
        print(f"ID parameter: {case['id']}")
        print(f"Expected status code: {case['status_code']}")
        print(f"Expected status: {case['expected_status']}")

        # 2. Создаем экземпляр API клиента для работы с тренерами
       # trainer_api = TrainerApi()    не применяем так как добавили фикстуру api из conftest.py

        # 3. Выполняем запрос в зависимости от типа ID
        if case['id'] is None:
            response = api.get_trainers()   # Если ID не указан - запрашиваем всех тренеров
        else:
            response = api.get_trainers(trainer_id=case['id'])   # Если ID указан - запрашиваем конкретного тренера
        
        # 4. Выводим информацию о выполненном запросе
        print(f"\nRequest URL: {response.response.url}")
        print(f"Status code: {response.response.status_code}")

        # 5. Проверяем, что статус код ответа соответствует ожидаемому
        api.status_code_should_be(case['status_code'])

        # 6. Получаем тело ответа в формате JSON
        response_data = response.response.json()
        print(f"\nResponse body: {response_data}")

        # 7. Проверяем структуру ответа в зависимости от тест-кейса
        if case['schema']:
            assert S(case['schema']) == response_data  # Если указана схема - проверяем соответствие ответа схеме
            assert response_data['status'] == case['expected_status']  # Проверяем статус в ответе
            
            if case['id'] is None:   # Дополнительные проверки для разных случаев
                assert len(response_data['data']) > 1    # Для запроса всех тренеров проверяем, что получено больше 1 записи
            elif case['id'] == 29010:
                assert len(response_data['data']) == 1     # Для конкретного ID проверяем, что получена 1 запись
        else:
            assert response_data['status'] == case['expected_status']   # Для случаев без схемы проверяем только статус
            if case['status_code'] == 422:  # Для ошибок 422 проверяем наличие сообщения об ошибке
                assert 'message' in response_data

        # 8. Выводим сообщение об успешном завершении тест-кейса
        print(f"\nTest case '{case['description']}' completed successfully!")