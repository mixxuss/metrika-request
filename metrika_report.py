import requests
from openpyxl import Workbook


def parse_input_file(path):
    with open(path, 'r') as text:
        text_lines_list = text.read().splitlines()
        return [text_line.split(' ') for text_line in text_lines_list]


def request_metrika_api_compare(params, url='https://api-metrika.yandex.ru/stat/v1/data/comparison'):
    api_response = requests.get(url, params)
    return api_response.text


def make_base_params(oauth_token='AQAAAAAT07WxAAQP6j2oJLgK80E0sM-fbCEx6eo', counter_id='26444823', is_pretty=True):
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


def output_to_xlsx():
    pass

def combine_params_list(params):
    pass


if __name__ == '__main__':
    dates = parse_input_file('dates.txt')
    sections = parse_input_file('sections.txt')
    print(dates)
    print(sections)
    '''for date in dates:
        for section in sections:
            print(group_params(base_params=make_base_params(),
                               output_params=make_output_params(),
                               date_params=make_date_params(date),
                               filter_params=make_filter_params(summ_filter([section]), summ_filter([section]) + ' AND (ym:u:totalVisitsDuration>=180)')))
    '''
    params = {'dimensions': 'ym:s:<attribution>SourceEngine', 'filters_b': "(ym:s:trafficSource=='organic') AND (ym:s:searchPhrase!@'baby' AND ym:s:searchPhrase!@'бэби' AND ym:s:searchPhrase!@'беби') AND (ym:s:startURLPathFull=*'/community/*') AND (ym:u:totalVisitsDuration>=180)", 'pretty': 'true', 'limit': 100, 'oauth_token': 'AQAAAAAT07WxAAQP6j2oJLgK80E0sM-fbCEx6eo', 'date2_a': '2017-01-29', 'date1_b': '2017-01-23', 'date1_a': '2017-01-23', 'metrics': 'ym:s:visits', 'date2_b': '2017-01-29', 'group': 'week', 'ids': '26444823', 'accuracy': 'high', 'filters_a': "(ym:s:trafficSource=='organic') AND (ym:s:searchPhrase!@'baby' AND ym:s:searchPhrase!@'бэби' AND ym:s:searchPhrase!@'беби') AND (ym:s:startURLPathFull=*'/community/*')"}
    print(request_metrika_api_compare(params))




    '''
    dates_list = [
        {'date1_a': '2017-01-23', 'date2_a': '2017-01-29', 'date1_b': '2017-01-23', 'date2_b': '2017-01-29'},
        {'date1_a': '2017-02-06', 'date2_a': '2017-02-12', 'date1_b': '2017-02-06', 'date2_b': '2017-02-12'}
    ]
    section_list = [['ym:s:startURLPathFull' '=*', '/community/*'],
                    ['ym:s:startURLPathFull', '=*', '/answers/*']]

    params = group_params(make_base_params(),
                          make_output_params(),
                          make_date_params('2017-02-09', '2017-02-10', '2017-02-09', '2017-02-10'),
                          make_filter_params(filters_a='(ym:s:trafficSource==\'organic\') AND (ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\') AND (ym:s:startURLPathFull=*\'/community/*\')',
                                             filters_b='(ym:s:trafficSource==\'organic\') AND (ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\') AND (ym:s:startURLPathFull=*\'/community/*\') AND (ym:u:totalVisitsDuration>=180)'))
    print(params)
    print(request_metrika_api_compare(params=params))
    '''

    '''
    OAuth_key = 'AQAAAAAT07WxAAQP6j2oJLgK80E0sM-fbCEx6eo'
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