import django_filters

from spanishtrainer_api.models import Word


class WordFilter(django_filters.FilterSet):
    class Meta:
        model = Word

        # exact match only, example: ?wordtype=8&level=1
        #fields = ['level', 'wordtype']

        # default for 'exact': case sensitive --> ?es=¡Buenas tArdes! is not found!
        # default for 'contains': ignore case
        # example: ?level__gt=2
        # example: ?level__lt=2
        # example 'exact': ?es=¡Hola!
        # example 'contains': ?es__contains=Hola
        # example 'contains': # ?es__contains=¡Buenas tardes!
        # example 'contains': # ?es__contains=¡buenas tardes!
        # example 'contains': # ?es__contains=tardes
        # !!! but: no word match: ?es__contains=el
        fields = {
            'level': ['exact', 'lt', 'gt', 'range'],
            'wordtype' : ['exact'],
            'es' : ['exact', 'contains']
        }