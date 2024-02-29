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
    DICTATOR_ROLE = 'Dictator'
    RECIPIENT_ROLE = 'Recipient'
    PROPOSER_ROLE = 'Proposer'
    RECEIVER_ROLE = 'Receiver'


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    matrix = subsession.get_group_matrix()
    if subsession.round_number == 1:
        for row in matrix:
            row.reverse()

        subsession.set_group_matrix(matrix)
            
            

            
class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=C.ENDOWMENT,
        label="I will keep",
    ),
    accepted = models.StringField(
    choices = [['0', 'SI'], ['10', 'NO']],
    label = "Acepta la oferta del proponente"
    ),


 


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.accepted == '0':
        p1.pay_off=group.kept
        p2.pay_off=C.ENDOWMENT - group.kept
    else:
        p1.pay_off=0
        p2.pay_off=0
    

def kept_choices(group):
    amount = range(0, int(C.ENDOWMENT + 1), 10)
    choices = list(zip(amount, amount))
    return choices



# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Accept(Page):
    form_model = 'group'
    form_fields = ['accepted']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title = "Waiting for other players..."
    body_text = "Please wait until all players have arrived before deciding on how to divide the amount."

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=C.ENDOWMENT - group.kept)

class UltimatumResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(
            offer=group.kept,
            accepted=group.accepted,
            kept=C.ENDOWMENT - group.kept
        )

page_sequence = [Introduction, Offer, Accept, ResultsWaitPage, UltimatumResults]

