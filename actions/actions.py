from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet, AllSlotsReset
import json

def sort_updated_date(file):
    with open(file, encoding='utf-8') as f:
        data = json.loads(f.read())
        data.sort(key=lambda x:x["data_atualizacao"], reverse=True)
    return data

# for obj in data:
#     try:
#         print(obj['modalidade'])
#         print()
#     except:
#         pass


class GetProfessorContact(Action):
    # categoria informações de servidores
    def name(self) -> Text:
        return "action_get_professor_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nome_professor = tracker.get_slot("professor_name")

        dispatcher.utter_message(
            text=f"{nome_professor}@riogrande.ifrs.edu.br")

        return[SlotSet("professor_name", None)]


class GetDocRegister(Action):

    def name(self) -> Text:
        return "action_get_doc_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_matricula = "https://sia.ifrs.edu.br/aplicacoes/frame/index.php"
        link_tutorial = "https://sia.ifrs.edu.br/aplicacoes/frame/index.php"

        dispatcher.utter_message(
            text=f"Para baixar o comprovante de matrícula você precisa acessar o link {link_matricula}")
        dispatcher.utter_message(
            text=f"Caso precise de alguma ajuda, assista o tutorial no link {link_tutorial}")

        return []


class GetClasses(Action):

    def name(self) -> Text:
        return "action_get_classes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_classes = "https://ifrs.edu.br/riogrande/ensino/retorno-do-calendario/horarios/"

        dispatcher.utter_message(
            text=f"Os horários de suas aulas e disciplinas você pode conferir aqui {link_classes}!")

        return []


class ClearSlots(Action):

    def name(self) -> Text:
        return "action_goodbye_and_clear_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        """ 
        Action com finalidade de limpar o slot para a solicitação ser atendida. Dessa forma é possível reiniciar a conversa e fazer novas solicitações
        """

        dispatcher.utter_message(response="utter_goodbye")
        return[AllSlotsReset()]

class GetCalendar(Action):

    def name(self) -> Text:
        return "action_get_calendar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """ 
        A action GetCalendar retorna ao usuário do Bot o calendário acadêmico, via link, do ano em vigência.
        Link único, uma vez que é um calendário para todos os cursos disponíveis no IFRS. A action recebe o valor do slot calendar
        """
    # variável link para inserir o calendário 
        link_calendar = "https://ifrs.edu.br/riogrande/wp-content/uploads/sites/16/2022/05/Calendario-Academico-Campus-Rio-Grande-2022-alterado-em-abril-2022.pdf"

        ano_corrente = 2022
        dispatcher.utter_message(
            text=f"Confira aqui o calendário acadêmico 👇")
        dispatcher.utter_message(attachment=link_calendar)

        return []


class GetCourses(Action):
    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        A action é chamada para validar a opção da modalidade do curso escolhida pelo usário, assim que validada ela dispacha paara o usuário botões de selecão do curso de acordo com a modalidade escolhida.
        Ao final da action, vai ser retornado também o preenchimento do slot (courses_modality_link) para ser utilizada na action seguinte (action_get_info_course) das Stories.
        """

        # buttons declaration
        buttons_integrado = [
            {"title": "Automação Industrial",
                "payload": '/courses{"courses_name": "automação"}'},
            {"title": "Fabricação Mecânica",
                "payload": '/courses{"courses_name": "fabricação"}'},
            {"title": "Informática para Internet",
                "payload": '/courses{"courses_name": "informática"}'},
            {"title": "Geoprocessamento",
                "payload": '/courses{"courses_name": "geoprocessamento"}'},
            {"title": "Eletrotécnica",
                "payload": '/courses{"courses_name": "eletrotécnica"}'},
            {"title": "Refrigeração",
                "payload": '/courses{"courses_name": "refrigeração"}'}
        ]
        buttons_subsequente = [
            {"title": "Automação Industrial",
                "payload": '/courses{"courses_name": "automação"}'},
            {"title": "Fabricação Mecânica",
                "payload": '/courses{"courses_name": "fabricação"}'},
            {"title": "Geoprocessamento",
                "payload": '/courses{"courses_name": "geoprocessamento"}'},
            {"title": "Eletrotécnica",
                "payload": '/courses{"courses_name": "eletrotécnica"}'},
            {"title": "Refrigeração",
                "payload": '/courses{"courses_name": "refrigeração"}'},
            {"title": "Enfermagem", "payload": '/courses{"courses_name": "enfermagem"}'}
        ]
        buttons_superior = [
            {"title": "Engenharia Mecânica",
                "payload": '/courses{"courses_name": "engenharia mecânica"}'},
            {"title": "Análise e Desenvolvimendo de Software",
                "payload": '/courses{"courses_name": "tads"}'},
            {"title": "Construção de Edifícios",
                "payload": '/courses{"courses_name": "tce"}'},
            {"title": "F. Pedagógica",
                "payload": '/courses{"courses_name": "formação pedagógica"}'},
            {"title": "F. Pedagógica não Licenciados",
                "payload": '/courses{"courses_name": "pedagógica não licenciados"}'}
        ]

        # variables declaration
        uri_base = "https://ifrs.edu.br/riogrande/cursos/"
        modality = tracker.get_slot("courses_modality").lower()

        modalities = {
            "integrado": {
                "link": "cursos-tecnicos-integrados/",
                "button": buttons_integrado,
            },
            "subsequente": {
                "link": "cursos-tecnicos-subsequentes/",
                "button": buttons_subsequente,
            },
            "superior": {
                "link": "cursos-superiores/",
                "button": buttons_superior,
            },
        }
        uri_modality = modalities[modality]["link"]

        # Dispatcher the button selector according with the chosen modality
        dispatcher.utter_message(
            text="Para qual curso gostaria de mais informações?",
            buttons=modalities[modality]["button"],
            button_type="vertical")

        complete_uri = uri_base+uri_modality

        return [SlotSet("courses_modality_link", complete_uri)]


class GetInfoCours(Action):

    def name(self) -> Text:
        return "action_get_info_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        A action valida o curso selecionado pelo usuário e busca o link de acordo com o botão clicado pelo usuário.
        Além de validar o curso, a action recebe o valor do slot (courses_modality_link) para interpolar com o endpoint de acordo com o curso selecionado.
        Por fim, despacha para o usuário a informação com o link correto.
        """

        courses = {
            "automação": "automacao-industrial/",
            "fabricação": "fabricacao-mecanica/",
            "informática": "informatica-para-internet/",
            "eletrotécnica": "eletrotecnica/",
            "geoprocessamento": "geoprocessamento/",
            "refrigeração": "refrigeracao-e-climatizacao/",
            "enfermagem": "enfermagem/",
            "engenharia mecânica": "engenharia-mecanica/",
            "tads": "tads/",
            "tce": "curso-superior-de-tecnologia-em-construcao-de-edificios/",
            "formação pedagógica": "curso-de-formacao-pedagogica/",
            "pedagógica não licenciados": "curso-de-formacao-pedagogica-para-graduados-nao-licenciados/"
        }

        course_name = tracker.get_slot("courses_name")
        course_modality = tracker.get_slot("courses_modality")
        link = tracker.get_slot("courses_modality_link")

        link += courses[course_name]

        msg = f"Segue o link de acesso para o curso {link}"

        dispatcher.utter_message(text=msg)

        return []

class ImformToDoRegister(Action):
    def name(self) -> Text:
        return "action_inform_do_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """
        Action para direcionar a forma de ingresso no IFRS. Recebe o valor do slot ingress_modality. Retorna ao usuário o link correto
        """
       
       # varáveis de banco de dados
       
        link_ingress = "https://ingresso.ifrs.edu.br/" #fica na aplicação
        ingress_modality= tracker.get_slot("ingress_modality")
       
        msg=f"Aqui você confere as formas de ingresso no IFRS {link_ingress} e {ingress_modality}"

        dispatcher.utter_message(text=msg)
        
        return []

class InformToRedoRegister(Action):
    def name(self) -> Text:
        return "action_inform_redo_register" 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """
        Action que mostra informações sobre a rematrícula nos cursos ofertados pelo IFRS
        """
    # buttons declaration
        buttons_integrado = [
            {"title": "Automação Industrial",
                "payload": '/courses{"courses_name": "automação"}'},
            {"title": "Fabricação Mecânica",
                "payload": '/courses{"courses_name": "fabricação"}'},
            {"title": "Informática para Internet",
                "payload": '/courses{"courses_name": "informática"}'},
            {"title": "Geoprocessamento",
                "payload": '/courses{"courses_name": "geoprocessamento"}'},
            {"title": "Eletrotécnica",
                "payload": '/courses{"courses_name": "eletrotécnica"}'},
            {"title": "Refrigeração",
                "payload": '/courses{"courses_name": "refrigeração"}'}
        ]
        buttons_subsequente = [
            {"title": "Automação Industrial",
                "payload": '/courses{"courses_name": "automação"}'},
            {"title": "Fabricação Mecânica",
                "payload": '/courses{"courses_name": "fabricação"}'},
            {"title": "Geoprocessamento",
                "payload": '/courses{"courses_name": "geoprocessamento"}'},
            {"title": "Eletrotécnica",
                "payload": '/courses{"courses_name": "eletrotécnica"}'},
            {"title": "Refrigeração",
                "payload": '/courses{"courses_name": "refrigeração"}'},
            {"title": "Enfermagem", "payload": '/courses{"courses_name": "enfermagem"}'}
        ]
        buttons_superior = [
            {"title": "Engenharia Mecânica",
                "payload": '/courses{"courses_name": "engenharia mecânica"}'},
            {"title": "Análise e Desenvolvimendo de Software",
                "payload": '/courses{"courses_name": "tads"}'},
            {"title": "Construção de Edifícios",
                "payload": '/courses{"courses_name": "tce"}'},
            {"title": "F. Pedagógica",
                "payload": '/courses{"courses_name": "formação pedagógica"}'},
            {"title": "F. Pedagógica não Licenciados",
                "payload": '/courses{"courses_name": "pedagógica não licenciados"}'}
        ]
        #variables declaration
        modality = tracker.get_slot("courses_modality").lower()

        modalities = {
            "integrado": {
                "link":"cursos-tecnicos-integrados/",
                "button": buttons_integrado,
                },
            "subsequente":{ 
                "link": "cursos-tecnicos-subsequentes/",
                "button": buttons_subsequente,
            },
            "superior": {
                "link":"cursos-superiores/",
                "button": buttons_superior,
            },
        }
        # Dispatcher the button selector according with the chosen modality
        dispatcher.utter_message(
            text="Para qual curso gostaria de obter informações sobre a rematricula?", 
            buttons=modalities[modality]["button"], 
            button_type="vertical")
             


        return []

class SystemType(Action):
    def name(self) -> Text:
        return "action_system_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        """
        Action que direciona para o link do sistema de rematricula de acordo com o nome do curso/modalidade
        """
        courses = {
            "automação": "automacao-industrial/",
            "fabricação": "fabricacao-mecanica/",
            "informática": "informatica-para-internet/",
            "eletrotécnica": "eletrotecnica/",
            "geoprocessamento": "geoprocessamento/",
            "refrigeração": "refrigeracao-e-climatizacao/",
            "enfermagem": "enfermagem/",
            "engenharia mecânica": "engenharia-mecanica/",
            "tads": "tads/",
            "tce": "curso-superior-de-tecnologia-em-construcao-de-edificios/",
            "formação pedagógica": "curso-de-formacao-pedagogica/",
            "pedagógica não licenciados": "curso-de-formacao-pedagogica-para-graduados-nao-licenciados/"
        }

        courses_name = tracker.get_slot("courses_name").title()
        courses_modality = tracker.get_slot("courses_modality").title()
        link_sia = "https://sia.ifrs.edu.br/aplicacoes/frame/index.php"
        link_sigaa = "https://sig.ifrs.edu.br/sigaa/verTelaLogin.do"
        link_superior = "https://www.youtube.com/watch?v=STZYUidrVAg&feature=youtu.be"
        link_subsequente = "https://www.youtube.com/watch?v=ndrJ-TY71wY&feature=youtu.be"


        with open("calendarios.json", encoding="utf-8") as file:
            data = json.loads(file.read())

        for order in data:
            try:
                if(order["modalidade"] == courses_modality and order["curso"] == courses_name):
                    if(order["courses_name"] == "tads"):  
                        link_sigaa = order["link_sigaa"]
                        msg=f"Para realizar a rematricula no {courses_name} acesse o Sigaa {link_sigaa}! Fique atento ao prazo que vai do dia 25/07 até 27/05/22!"
                        dispatcher.utter_message(text=msg)
                        break
                    else: 
                        link_sia = order["link_sia"]
                        msg=f"Para realizar a rematrícula no {courses_name} acesse o Sia {link_sia}! Fique atento ao prazo que vai do dia 25/07 até 27/05/22! Em caso de dúvidas de como acessar o sistema veja o tutorial {link_superior} e {link_subsequente} "
                        dispatcher.utter_message(text=msg)
                        break
            
            except:
                pass 
        return []

class WhatBotDo(Action):
    def name(self) -> Text:
        return "action_what_bot_do"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=f"Tu pode me solicitar:👇\n➡️ Contato dos professores\n➡️ Calendário acadêmico\n➡️ Cursos disponíveis\n➡️ Comprovante de matrícula\n➡️ Informações sobre as aulas\n➡️ Inscrições\n➡️ Como fazer a rematrícula\n➡️ Requerimentos/Formulários")

        return []


class Requirements(Action):
    def name(self) -> Text:
        return "action_get_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # difine arquivo padrão para busca do dado ordenado por ultima atualização
        data = sort_updated_date("../chatbot_IF/requerimentos.json")
        # recebe slot pelo input do usuário
        requirement = tracker.get_slot("requirements").lower()    
        # busca por todas as recorrencias do requerimento no json
        req = [x for x in data if x['nome_requerimento']==requirement and x['visivel']==True]
        # recebe a ultima atualização do requerimento
        try:
            updated_req = req[0]
            text = updated_req["descricao"]
            link = updated_req["arquivo_link"]
            data_inicio = updated_req["data_inicio"]
            data_fim = updated_req["data_fim"]
            requirement = requirement.title()

            dispatcher.utter_message(text=text)
            dispatcher.utter_message(text=f"Lembrando que o prazo para preenchimento vai de {data_inicio} até {data_fim}")
            dispatcher.utter_message(
                text=f'Segue o [link]({link}) para o formulário!')
        except:
            dispatcher.utter_message(text=f'O requerimento \n`"{requirement}"` \nestá indisponível no momento')


        return [SlotSet("requirements", None)]


class SystemsTutorial(Action):
    def name(self) -> Text:
        return "action_get_system_tutorials"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        # variaveis setadas a partir de slots
        system = tracker.get_slot("system")

        # retorno de infomações do json
        with open("tutoriais.json", encoding='utf-8') as f:
            data = json.loads(f.read())
            data.sort(key=lambda x:x[""])

        # description = 

        #  descricao
        #  link_acesso
        #  link_recurso(video/pdf)
        #  data_atualização
        #  visivel
        # pass

def clean_name(name):
    return "".join([c for c in name if c.isalpha()])


class NameFormValidate(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """
        A action NameFormValidate serve para a validação do name form. Para informar que ocorreu um possível erro na informação da mensagem ou nome, retornando em caso de erro nome como None. Também serve para o preenchimento do respectivo slot
        """
        name = clean_name(slot_value).title()
        if len(name) == 0:
            dispatcher.utter_message(
                text="Não entendi, pode ter sido um erro de digitação")
            return {"name": None}
        return {"name": name}


class ProfessorNameFormValidate(FormValidationAction):
    def name(self) -> Text:
        return "validate_professor_name_form"

    def validate_professor_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        name = clean_name(slot_value).title()
        if len(name) == 0:
            dispatcher.utter_message(
                text="Não entendi, pode ter sido um erro de digitação")
            return {"professor_name": None}
        return {"professor_name": name}
