from celery import Celery
from service.convert_service import ConvertNumberService
from service.parameter_service import ParameterService

parameter_service = ParameterService()
redis_url = parameter_service.get_parameter('redis_url')

app = Celery('tasks', broker=redis_url, backend=redis_url)

@app.task(serializer='json')
def convert_to_word(number):
    convert_number_service = ConvertNumberService()
    return convert_number_service.to_words(number).to_json()


