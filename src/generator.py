
# https://www.avito.ru/all/avtomobili/bmw?p=3&s=104
# https://auto.ru/cars/bmw/all/?sort=cr_date-desc&page=2
# https://auto.drom.ru/bmw/all/page2/

def generate_params():

    url_templates = {
        'autoru': "https://auto.ru/cars/{brand}/all/?sort=cr_date-desc&page={page}",
        'avito': "https://www.avito.ru/all/avtomobili/{brand}?p={page}&s=104",
        'drom': "https://auto.drom.ru/{brand}/all/page{page}/"
    }

    params = {
        'url_template': url_templates['autoru'],
        'brand': 'bmw',
        'page_from': 1,
        'page_to': 10
    }

    return params