import requests
from openpyxl import Workbook


def parse_input_file(path):
    with open(path, 'r') as text:
        text_lines_list = text.read().splitlines()
        return [text_line.split(' ') for text_line in text_lines_list]


def request_metrika_api_compare(params, url='https://api-metrika.yandex.ru/stat/v1/data/comparison'):
    api_response = requests.get(url, params)
    return api_response.json()


def make_base_params(oauth_token='PUT', counter_id='26444823', is_pretty=True):
    return {
        'oauth_token': oauth_token,
        'ids': counter_id,
        'pretty': str(is_pretty).lower()
    }


def make_output_params(metrics='ym:s:visits', dimensions='ym:s:<attribution>SourceEngine',
                       limit=100, accuracy='high', group='week'):
    return {
        'metrics': metrics,
        'dimensions': dimensions,
        'limit': limit,
        'accuracy': accuracy,
        'group': group
    }


def make_date_params(dates_list):
    return {
        'date1_a': dates_list[0],
        'date2_a': dates_list[1],
        'date1_b': dates_list[2],
        'date2_b': dates_list[3]
    }


def make_filter_params(filters_a, filters_b):
    return {
        'filters_a': filters_a,
        'filters_b': filters_b
    }


def group_params(base_params, output_params, date_params, filter_params):
    all_params = {}
    all_params.update(base_params)
    all_params.update(output_params)
    all_params.update(date_params)
    all_params.update(filter_params)
    return all_params


def summ_filter(section):
    return '(ym:s:trafficSource==\'organic\') AND (ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\') AND {}'.format(make_any_filter(section))


def make_any_filter(param_list):
    if len(param_list) > 1:
        section_param = ' AND '.join(['{}{}\'{}\''.format(params[0], params[1], params[2]) for params in param_list])
        return '({})'.format(section_param)
    else:
        for params in param_list:
            return '({}{}\'{}\')'.format(params[0], params[1], params[2])


def create_xlsx_file():
    excel_file = Workbook()
    return excel_file


def create_xlsx_worksheet(excel_file, date):
    ex_page = excel_file.create_sheet('{}-{}'.format(date[0], date[1]))
    return ex_page


def output_to_xlsx_worksheet(response, ex_page, row, section_list):
    # for response in response_func:
    ex_page['A{}'.format(row)] = section_list[2]
    ex_page['B{}'.format(row)] = 'ПС'
    try:
        total_a = response['totals']['a'][0]
    except IndexError:
        total_a = 0
    ex_page['C{}'.format(row)] = total_a
    try:
        total_b = response['totals']['b'][0]
    except IndexError:
        total_b = 0
    ex_page['D{}'.format(row)] = total_b
    try:
        ex_page['E{}'.format(row)] = '{}%'.format(round(total_b / total_a * 100))
    except ZeroDivisionError:
        ex_page['E{}'.format(row)] = 'Cant calc'
    row += 1
    try:
        ex_page['B{}'.format(row)] = response['data'][0]['dimensions'][0]['name']
    except IndexError:
        ex_page['B{}'.format(row)] = 0
    try:
        first_a = response['data'][0]['metrics']['a'][0]
    except IndexError:
        first_a = 0
    ex_page['C{}'.format(row)] = first_a
    try:
        first_b = response['data'][0]['metrics']['b'][0]
    except IndexError:
        first_b = 0
    ex_page['D{}'.format(row)] = first_b
    try:
        ex_page['E{}'.format(row)] = '{}%'.format(round(first_b / first_a * 100))
    except ZeroDivisionError:
        ex_page['E{}'.format(row)] = 'Cant calc'
    row += 1
    try:
        ex_page['B{}'.format(row)] = response['data'][1]['dimensions'][0]['name']
    except IndexError:
        ex_page['B{}'.format(row)] = 0
    try:
        second_a = response['data'][1]['metrics']['a'][0]
    except IndexError:
        second_a = 0
    ex_page['C{}'.format(row)] = second_a
    try:
        second_b = response['data'][1]['metrics']['b'][0]
    except IndexError:
        second_b = 0
    ex_page['D{}'.format(row)] = second_b
    try:
        ex_page['E{}'.format(row)] = '{}%'.format(round(second_b / second_a * 100))
    except ZeroDivisionError:
        ex_page['E{}'.format(row)] = 'Cant calc'
    row += 1
    return ex_page, row


def save_xlsx_file(excel_file, filename='Metrika.xlsx'):
    excel_file.save(filename)


if __name__ == '__main__':
    dates = parse_input_file('dates.txt')
    sections = parse_input_file('sections.txt')
    print(dates)
    print(sections)
    excel_file = create_xlsx_file()

    for date in dates:
        ex_page = create_xlsx_worksheet(excel_file, date)
        row = 1
        section_number_from_list = 1
        for section in sections:
            params = group_params(base_params=make_base_params(),
                               output_params=make_output_params(),
                               date_params=make_date_params(date),
                               filter_params=make_filter_params(summ_filter([section]), summ_filter([section]) + ' AND (ym:u:totalVisitsDuration>=180)'))
            print(params)
            response = request_metrika_api_compare(params)
            print(response)
            section_number_from_list += 1
            ex_page, row = output_to_xlsx_worksheet(response, ex_page, row, section_list=section)
    save_xlsx_file(excel_file)

    # params = {'dimensions': 'ym:s:<attribution>SourceEngine', 'filters_b': "(ym:s:trafficSource=='organic') AND (ym:s:searchPhrase!@'baby' AND ym:s:searchPhrase!@'бэби' AND ym:s:searchPhrase!@'беби') AND (ym:s:startURLPathFull=*'/community/*') AND (ym:u:totalVisitsDuration>=180)", 'pretty': 'true', 'limit': 100, 'oauth_token': 'AQAAAAAT07WxAAQP6j2oJLgK80E0sM-fbCEx6eo', 'date2_a': '2017-01-29', 'date1_b': '2017-01-23', 'date1_a': '2017-01-23', 'metrics': 'ym:s:visits', 'date2_b': '2017-01-29', 'group': 'week', 'ids': '26444823', 'accuracy': 'high', 'filters_a': "(ym:s:trafficSource=='organic') AND (ym:s:searchPhrase!@'baby' AND ym:s:searchPhrase!@'бэби' AND ym:s:searchPhrase!@'беби') AND (ym:s:startURLPathFull=*'/community/*')"}
    # response = request_metrika_api_compare(params)
    # print(response['data'])
    # print(response['data'][0]['dimensions'][0]['name'], response['data'][0]['metrics']['a'], response['data'][0]['metrics']['b'])
    # print(response['totals']['a'][0], response['totals']['b'][0])
    # output_to_xlsx(response)

    '''
    OAuth_key = 'PUT'
    ids = '26444823'
    url = 'https://api-metrika.yandex.ru/stat/v1/data/comparison'
    params = {
        'oauth_token': OAuth_key,
        'ids': ids,
        'pretty': 'true',
        'accuracy': 'high',
        'group': 'week',
        'limit': 1000,
        'metrics': 'ym:s:visits',
        'dimensions': 'ym:s:<attribution>SourceEngine',
        'date1_a': '2017-02-09',
        'date2_a': '2017-02-10',
        'filters_a': '(ym:s:trafficSource==\'organic\') '
                     'AND (ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\') '
                     'AND (ym:s:startURLPathFull=*\'/community/*\')',
        'date1_b': '2017-02-09',
        'date2_b': '2017-02-10',
        'filters_b': '(ym:s:trafficSource==\'organic\') '
                     'AND (ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\') '
                     'AND (ym:s:startURLPathFull=*\'/community/*\') '
                     'AND (ym:u:totalVisitsDuration>=180)',
    }
    response = requests.get(url, params=params)
    print(response.text)
    '''