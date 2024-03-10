from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'Encuesta'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='¿Qué edad tiene?', min=14, max=100)
    gender = models.StringField(
        choices=[['Masculino', 'Masculino'], ['Femenino', 'Femenino']],
        label='¿Cuál es su género?',
        widget=widgets.RadioSelect,
    )
    estudiante = models.StringField(
        choices=[['Estudiante', 'Estudiante'], ['Egresado', 'Egresado']],
        label='¿Usted es estudiante o egresado?',
        widget=widgets.RadioSelect,
    )
    universidad = models.StringField(
        choices=[['UDEP', 'UDEP'],
                 ['UP', 'UP'],
                 ['PUCP', 'PUCP'],
                 ['UNMSM', 'UNMSM'],
                 ['UPC', 'UPC'],
                 ['U de Lima', 'U de Lima'],
                 ['UNTRM', 'UNTRM'],
                 ['ESAN', 'ESAN'],
                 ['UNPRG', 'UNPRG'],
                 ['Otro', 'Otro']],
        label='Escoja su universidad:',
        widget=widgets.RadioSelect,
    )
    carrera = models.StringField(
        choices=[['Economía', 'Economía'],
                 ['Finanzas', 'Finanzas'],
                 ['Ingeniería', 'Ingeniería'],
                 ['Otro', 'Otro']],
        label='Escoja su carrera:',
        widget=widgets.RadioSelect,
    )
    ingreso = models.StringField(
        choices=[['No trabajo', 'No trabajo'],
                 ['S/0 a S/1025', 'S/0 a S/1025'], 
                 ['S/1025 a S/1500', 'S/1025 a S/1500'],
                 ['S/1500 a S/2500', 'S/1500 a S/2500'],
                 ['S/2500 a más', 'S/2500 a más']],
        label='¿Cuál es su ingreso percibido?',
        widget=widgets.RadioSelect,
    )

# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'estudiante','universidad','carrera','ingreso']

class gratefulness(Page):
    pass

page_sequence = [Demographics, gratefulness]