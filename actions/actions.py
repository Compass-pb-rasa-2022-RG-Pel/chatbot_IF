from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet


class BuscarProfessor(Action):

    def name(self) -> Text:
        return "action_buscar_professor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nome_professor = tracker.get_slot("professor_name")

        dispatcher.utter_message(
            text=f"{nome_professor}@riogrande.ifrs.edu.br")

        return[SlotSet("professor_name", None)]


class BuscarFaq(Action):

    def name(self) -> Text:
        return "action_faq_comprovate"

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


class BuscarClasses(Action):

    def name(self) -> Text:
        return "action_buscar_classes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_classes = "https://ifrs.edu.br/riogrande/ensino/retorno-do-calendario/horarios/"

        dispatcher.utter_message(
            text=f"Os horários de suas aulas e disciplinas você pode conferir aqui {link_classes}!")

        return []


class BuscarCalendar(Action):

    def name(self) -> Text:
        return "action_get_calendar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_calendar = "https://ifrs.edu.br/riogrande/ensino/calendario-academico/"

        dispatcher.utter_message(
            text=f"Confira aqui seu calendário acadêmico {link_calendar}")

        return []


class BuscarCursos(Action):
    def name(self) -> Text:
        return "action_buscar_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_cursos = "https://ifrs.edu.br/riogrande/cursos/"

        dispatcher.utter_message(
            text=f"Confira aqui os cursos disponíveis no IFRS {link_cursos}")

        return []


class DocToRegister(Action):
    def name(self) -> Text:
        return "action_inform_do_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link = "https://ingresso.ifrs.edu.br/"

        dispatcher.utter_message(
            text=f"Através do link abaixo tu pode te matricular em um dos nossos cursos:")
        dispatcher.utter_message(
            url=link)

        return []


class DocToRedoRegister(Action):
    def name(self) -> Text:
        return "action_inform_redo_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        link_tutorial = "https://www.youtube.com/watch?v=STZYUidrVAg"
        link = "https://sia.ifrs.edu.br/aplicacoes/frame/index.php"

        dispatcher.utter_message(
            text=f"As rematrículas dos cursos das modalidades **Superior** e **Subsequente** ocorrerão dos dias **25/07** à **27/07** através do link abaixo: ")
        dispatcher.utter_message(url=link)
        dispatcher.utter_message(
            text="Caso esteja com dificuldades consulte o link abaixo 👇")
        dispatcher.utter_message(url=link_tutorial)

        return []


class BuscarEstagios(Action):
    def name(self) -> Text:
        return "action_buscar_internship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        link_estagio = "https://ifrs.edu.br/riogrande/extensao/estagios/"

        dispatcher.utter_message(
            text=f"Confira aqui maiores informações sobre estágios no IFRS! {link_estagio}")

        return []


class BotDo(Action):
    def name(self) -> Text:
        return "action_bot_do"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=f"Tu pode me solicitar:👇\n➡️ Contato dos professores\n➡️ Calendário acadêmico\n➡️ Cursos disponíveis\n➡️ Informações sobre estágio\n➡️ Comprovante de matrícula\n➡️ Informações sobre as aulas\n➡️ Documentos para matricula\n➡️ Como fazer a rematrícula")

        return []

# validate name


def clean_name(name):
    return "".join([c for c in name if c.isalpha()])


class ValidaNomeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        name = clean_name(slot_value).title()
        if len(name) == 0:
            dispatcher.utter_message(text="Não entendi, pode ter sido um erro de digitação")
            return {"name": None}
        return {"name": name}
class ValidaNomeForm(FormValidationAction):
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
            dispatcher.utter_message(text="Não entendi, pode ter sido um erro de digitação")
            return {"professor_name": None}
        return {"professor_name": name}
