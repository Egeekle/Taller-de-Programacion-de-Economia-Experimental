from otree.api import *



doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    # Initial amount allocated to the dictator
    ENDOWMENT = cu(100)
    DICTATOR_ROLE= "El Proponente"
    RECIPIENT_ROLE= "El Receptor"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    matrix= subsession.get_group_matrix()
    if subsession.round_number== 2:
        for row in matrix:
            row.reverse()
        subsession.set_group_matrix(matrix)

class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=C.ENDOWMENT,
        label="Me quedaré con",
    )

    accepted = models.StringField(
       choices= [["Sí", "Sí"], ["No","No"]],
       label= "¿Acepta la oferta del proponente?",
       widget=widgets.RadioSelect,
    )

class Player(BasePlayer):
   pass

# FUNCTIONS
def set_payoffs(group: Group):
    if group.accepted == "No":
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        p1.payoff= 0
        p2.payoff= 0
        
    else:
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        p1.payoff = group.kept
        p2.payoff = C.ENDOWMENT - group.kept


# Agregar funciones avanzadas

def kept_choices(group):
    montos = range(0,int(C.ENDOWMENT)+1,10)
    lista = list(montos)
    choices = lista
    return(choices)

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class Accept(Page):
    form_model = 'group'
    form_fields = ['accepted']

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer= C.ENDOWMENT - group.kept)

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text= "Espere, por favor."
    body_text="Esperando a que su compañero(a) decida."

class SecondWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.accepted=="Sí":
            return dict(offer= C.ENDOWMENT - group.kept)
        else:
            return dict(offer=0)

page_sequence = [Introduction, Offer,SecondWaitPage, Accept, ResultsWaitPage,Results]
