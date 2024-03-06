from otree.api import *

import random


doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""

class C(BaseConstants):
    NAME_IN_URL = 'bargaining'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    AMOUNT_SHARED = cu(100)
    #ROLES
    SELLER_ROLE = 'El Vendedor'
    BUYER_ROLE = 'El Comprador'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_requests = models.CurrencyField()
    Oferta = models.CurrencyField(
        min=0,
        max=100,
        label='Establezca su oferta inicial (entre 0,00 FIC y 100,00 FIC)'
    )
    Contraoferta=models.CurrencyField(
    min=0,
    max=100,
    label='Establezca su propuesta de contraoferta (entre 0,00 FIC y 100,00 FIC)'
    )
    Acepta=models.StringField(
        label='¿Acepta la contraoferta? (si/no)',
        choices=[['Sí','Si'],['No','No']],
        widget=widgets.RadioSelect
    )
    Value_enterprise=models.IntegerField()
    Proportion=models.FloatField()

class Player(BasePlayer): #eliminar
    pago_final= models.CurrencyField()
    

# FUNCTIONS    

def set_payoffs(group: Group):
    players = group.get_players()
    comprador=group.get_player_by_role(C.BUYER_ROLE)
    vendedor=group.get_player_by_role(C.SELLER_ROLE) 
    if group.Acepta == 'Sí':
        vendedor.payoff=group.Contraoferta-(group.Value_enterprise * group.Proportion)
        comprador.payoff=group.Value_enterprise-group.Contraoferta        
    else:
        for p in players:
            p.payoff = cu(0)


def creating_session(subsession):
    subsession.group_randomly(fixed_id_in_group=True)
    for grupos in subsession.get_groups():
        grupos.Value_enterprise = random.randrange(10,95,5) 
        grupos.Proportion=(random.randrange(1,10,1))/10

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1
    @staticmethod
    def vars_for_template(player: Player):
        group=player.group
        return dict(
            rol_vendedor=C.SELLER_ROLE,
            rol_comprador=C.BUYER_ROLE)
class Oferta(Page):
    form_model = 'group'
    form_fields = ['Oferta']
    @staticmethod
    def vars_for_template(player: Player):
        group=player.group
        return dict(
            valor_empresa=group.Value_enterprise,
            proporcion=group.Proportion)
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
class WaitPage1(WaitPage):
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."
    
class Contraoferta(Page):
    form_model = 'group'
    form_fields = ['Contraoferta']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
    @staticmethod
    def vars_for_template(player: Player):
        group=player.group
        return dict(
            oferta1 = group.Oferta,
            proporcion1= group.Proportion
        )
    
class WaitPage2(WaitPage):
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."

class Decision(Page):
    form_model='group'
    form_fields=['Acepta']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    @staticmethod
    def vars_for_template(player: Player):
        group=player.group
        return dict(
            valor_empresa=group.Value_enterprise,
            proporcion1=group.Proportion,
            contraoferta1=group.Contraoferta
        )
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."
    
class Results(Page):
    def vars_for_template(player: Player):
        group=player.group
        return dict(proporcion=group.Proportion,valor_empresa=group.Value_enterprise,oferta1=group.Oferta,contraoferta1=group.Contraoferta,pago_ronda=player.payoff )
            

class Resultado_Final(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        participant=player.participant
        player.pago_final=participant.payoff/C.NUM_ROUNDS
        return dict(pago_final=player.pago_final)
        
page_sequence = [Introduction, Oferta,WaitPage1 ,Contraoferta,WaitPage2,Decision,ResultsWaitPage, Results,Resultado_Final]

