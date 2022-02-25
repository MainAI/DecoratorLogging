import requests
import logging


def logging_decorator(file_path):
    def _wrapped(old_function):
        def new_function(*args, **kwargs):
            FORMAT = '%(asctime)s - %(f_name)s - %(arg_func)s - %(res_func)s'
            arg_func = f'{args}{kwargs}'
            logging.basicConfig(filename=file_path, filemode='w', level='INFO', format=FORMAT)
            result = old_function(*args, **kwargs)
            f_name = old_function.__name__
            d = {'f_name': f_name, 'arg_func': arg_func, 'res_func': result}
            logging.info('run this function', extra=d)
            return result
        return new_function
    return _wrapped


logging_decorator_filename = logging_decorator('log_records.txt')


class SuperHero:
    """ Get information about superhero from superhero API """

    def __init__(self, token):
        self.token = token

    @logging_decorator_filename
    def _requests_id(self, superhero_list):
        """ Search id superhero by name inside superhero_list, generate id_dict = {name: id} """
        id_dict = {}
        for person in superhero_list:
            url = f"https://superheroapi.com/api/{self.token}/search/{person}"
            response = requests.get(url=url)
            temp = response.json()
            id_dict[person] = temp['results'][0]['id']
        return id_dict

    @logging_decorator_filename
    def _intelligence_by_name(self, superhero_list):
        """ Create intellig_dict = {name: intelligence} """
        intellig_dict = {}
        for name, id_person in self._requests_id(superhero_list=superhero_list).items():
            url = f"https://superheroapi.com/api/{self.token}/{id_person}/powerstats"
            resp = requests.get(url=url)
            result = resp.json()
            intellig_dict[name] = result['intelligence']
        return intellig_dict

    @logging_decorator_filename
    def who_max_intelligence(self, superhero_list):
        """ print name max intelligence hero """
        sorted_list = sorted(self._intelligence_by_name(superhero_list=superhero_list).items(),
                             key=lambda items: items[1])
        print(f"Самый умный супергерой: {sorted_list[0][0]}!")
        return


if __name__ == '__main__':
    TOKEN = input('Insert token:')
    superhero = ['Hulk', 'Captain America', 'Thanos']
    super_person = SuperHero(TOKEN)
    super_person.who_max_intelligence(superhero)
