import random

from datetime import datetime


def generate_params():

    url_templates = {
        'autoru': "https://auto.ru/cars/{brand}/all/?sort=cr_date-desc&page={page}",
        'avito': "https://www.avito.ru/all/avtomobili/{brand}?p={page}&s=104",
        'drom': "https://auto.drom.ru/{brand}/all/page{page}/"
    }

    car_brands = ['bmw', 'volkswagen', 'vaz', 'audi', 'honda', 'kia', 'lexus', 'hyundai', 'mazda',
                  'mercedes', 'mitsubishi', 'nissan', 'opel', 'porsche', 'skoda', 'toyota', 'ford']

    params = {
        'url_template': url_templates['autoru'], # TODO add random choice from url_templates keys
        'brand': random.choice(car_brands),
        'page_from': 1,
        'page_to': 32,
        "today": str(datetime.now().date())
    }

    return params