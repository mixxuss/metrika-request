import requests


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


def make_date_params(start_date_a, finish_date_a, start_date_b, finish_date_b):
    return {
        'date1_a': start_date_a,
        'date2_a': finish_date_a,
        'date1_b': start_date_b,
        'date2_b': finish_date_b
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


def make_filter(section_list, traffic_source="\'organic\'", minus_word_list=['baby', 'беби', 'бэби']):
    minus_words = '(ym:s:searchPhrase!@\'baby\' AND ym:s:searchPhrase!@\'бэби\' AND ym:s:searchPhrase!@\'беби\')'
    return '(ym:s:trafficSource=={}) AND {} AND {}'.format(traffic_source, minus_words, section_list)


def make_minus_word_param(minus_words_list=['baby', 'беби', 'бэби']):
    return ' AND '.join(['ym:s:searchPhrase!@\'{}\''.format(minus_word) for minus_word in minus_words_list])


def make_params_list(params):
    pass


if __name__ == '__main__':
    make_minus_word_param()


    '''
    dates_list = [
        {'date1_a': '2017-02-09', 'date2_a': '2017-02-10', 'date1_b': '2017-02-09', 'date2_b': '2017-02-10'},
        {'date1_a': '2017-02-06', 'date2_a': '2017-02-08', 'date1_b': '2017-02-06', 'date2_b': '2017-02-08'}
    ]
    section_list = [{'ym:s:startURLPathFull=*':'/community/*'},
                    {'ym:s:startURLPathFull=*':'/answers/*'}]

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