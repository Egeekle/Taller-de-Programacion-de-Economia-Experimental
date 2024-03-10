from otree.api import *

# Se importa el comando para generar numeros aleatorios
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
    seller_role= "el vendedor"
    buyer_role= "el comprador"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_requests = models.CurrencyField()
    Oferta= models.CurrencyField(
        min=0,
        max=100,
        label="Establezca su oferta inicial (entre 0,00 FIC y 100,00 FIC):"
    )
    Contraoferta= models.CurrencyField(
        min=0,
        max=100,
        label="Establezca una propuesta de contraoferta (entre 0,00 FIC y 100,00 FIC):"
    )
    Acepta=models.StringField(
        label="¿Acepta la contraoferta propuesta?",
        choices= [["Sí","Sí"],
                  ["No","No"]],
        widget=widgets.RadioSelect
    )
    Valor_empresa= models.IntegerField()
    Proporcion= models.FloatField()


class Player(BasePlayer):
    pago_final= models.CurrencyField()


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    vendedor= group.get_player_by_id(1)
    comprador= group.get_player_by_id(2)
    if group.Acepta == "Sí":
       vendedor.payoff= group.Contraoferta - (group.Valor_empresa * group.Proporcion)
       comprador.payoff= group.Valor_empresa - group.Contraoferta
    else:
        for p in players:
            p.payoff = cu(0)


def creating_session(subsession): #aleatorizar grupos y otros valores
    subsession.group_randomly(fixed_id_in_group=True)
    for grupos in subsession.get_groups():
        grupos.Valor_empresa= random.randrange(10,95,5)
        grupos.Proporcion= (random.randrange(1,10,1))/10



# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(rol_vendedor= C.seller_role,
                    rol_comprador= C.buyer_role,
                    n_rondas= C.NUM_ROUNDS)


class Oferta_page(Page):
    form_model="group"
    form_fields=["Oferta"]

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(valor_empresa= group.Valor_empresa,
                    proporcion1= group.Proporcion,
                    valoracion_vendedor= round(group.Valor_empresa*group.Proporcion,2)
                    )

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class WaitPage1(WaitPage):
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."

class Contraoferta_page(Page):
    form_model="group"
    form_fields=["Contraoferta"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(oferta1= group.Oferta,
                    proporcion1= group.Proporcion)

class WaitPage2(WaitPage):
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."

class Decision(Page):
    form_model="group"
    form_fields=["Acepta"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(valor_empresa= group.Valor_empresa,
                    proporcion1= group.Proporcion,
                    contraoferta1= group.Contraoferta,
                    valoracion_vendedor= round(group.Valor_empresa*group.Proporcion,2)
                    )

class Request(Page):
    form_model = 'player'
    form_fields = ['request']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text= "Espere, por favor."
    body_text="Esperando a que decida el otro jugador."


class Results(Page):
    def vars_for_template(player: Player):
        group = player.group
        return dict(oferta1= group.Oferta,
                    contraoferta1= group.Contraoferta,
                    pago_ronda= player.payoff)
    
    
class ResultadoFinal(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):
        participant=player.participant
        player.pago_final= participant.payoff / C.NUM_ROUNDS
        return dict(
            pago_final= player.pago_final
        )


page_sequence = [Introduction, Oferta_page, WaitPage1,Contraoferta_page,WaitPage2,Decision,ResultsWaitPage,Results, ResultadoFinal] 
