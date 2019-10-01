# -*- coding: utf-8 -*-
from __future__ import with_statement
import smtplib
import sys
from thehive4py.api import TheHiveApi
from jinja2 import Template
from cortexutils.responder import Responder
sys.path.append("..")
from email.message import EmailMessage
from thehive4py.query import *
from email import encoders


class Reporter(Responder):
    """
    This Reporter class automates the effort of producing a case-report and optionally all of its associated data,
    such as observables and tasks.
    The primary function of this algorithm, is to take a JSON-structure gathered from TheHive's API, and filter it
    as per the provided filter-parameters given on activation.

    The algorithm assumes, that the dataset that's worked on, is either of any primitive type like int and string or
    a specific data structure list or dict, hence the dict- and list-builders.

    In short, the algorithm generates a new filtered tree-structure in JSON-format, which can be N-wide and N-deep.
    """
    def __init__(self):
        Responder.__init__(self)
        self.case_data_filter = ["endDate", "startDate", "title", "createdAt", "caseId", "pap", "tlp", "severity",
                                 "owner", "createdBy", "updatedBy", "summary", "tags", "resolutionStatus",
                                 "impactStatus", "status", "customFields"]
        self.case_observables_filter = ["data", "dataType", "sighted", "tags", "createdAt",
                    "createdBy", "pap", "tlp", "ioc", "startDate", "status"]
        self.case_tasks_filter = ["caseTasks", "updatedBy", "createdAt", "flag", "description",
              "title", "createdBy", "updatedAt", "order", "status", "group"]

        self.api_key = self.get_param('config.api_key', None, 'Missing API-key')
        self.https_address = self.get_param('config.https_address', 'localhost')
        self.https_port = self.get_param('config.https_port', 9000, 'Missing thehive port')
        self.smtp_host = self.get_param('config.smtp_host', 'localhost')
        self.smtp_port = self.get_param('config.smtp_port', '25')
        self.mail_from = self.get_param('config.from', None, 'Missing sender email address')
        self.api = TheHiveApi(f"https://{self.https_address}:{self.https_port}", self.api_key)

    def get_case_data(self, case_id):
        """
        Contacts the TheHive-API, and gets the case-data,. (Maybe not useful once the program is integrated with Cortex,
        as the JSON-object given upon a call of the responder, is matching the fetched data from this function.

        Args:
            case_id (str): id of the case to be gathered from

        Returns:
            str: returns a string in JSON-format
        """
        case_data = self.api.get_case(case_id=case_id)

        if case_data.status_code == 200:
            json_data = {
                "caseData": case_data.json()
            }

            return json_data
        else:
            print(f'ko: {case_data.status_code}/{case_data.text}')
            sys.exit(0)

    def get_case_observables(self, case_id: str):
        """
        Contacts the TheHive-API, and gets the observables from given case_id

        Args:
            case_id (str): id of the case to be gathered from

        Returns:
            str: returns a string in JSON-format
        """
        case_data = self.api.get_case_observables(case_id=case_id)

        if case_data.status_code == 200:
            json_data = {
                "caseObservables": case_data.json()
            }

            return json_data
        else:
            print(f'ko: {case_data.status_code}/{case_data.text}')
            sys.exit(0)

    def get_case_tasks(self, case_id: str):
        """
        Contacts the TheHive-API, and gets the associated tasks from the given case-id.

        Args:
            case_id (str): id of the case to be gathered from

        Returns:
            str: returns a string in JSON-format
        """
        case_data = self.api.get_case_tasks(case_id=case_id)

        if case_data.status_code == 200:
            json_data = {
                "caseTasks": case_data.json()
            }

            return json_data
        else:
            print(f'ko: {case_data.status_code}/{case_data.text}')
            sys.exit(0)

    def dict_builder(self, data: dict, filter: list, result_obj: object = None, path: list = None):
        """
        1 of 2 algorithms to recursively generate a JSON-structure, which is filtered by the provided filters given upon
        activation of this module in Cortex.

        Args:
            data (dict): new node of values, which can contain either a new node(list or dict) or a leaf (primitive type)
            filter: (list): target list of values which the new JSON-should contain
            result_obj: the new JSON-object, which holds the current progress of the algorithm
            path: used to keep track of the depth of the new JSON-object, to maintain the original object-structure

        Examples:
            FILTER_CANDIDATES = ["caseData", "title", "description"] - This takes all the data from caseData dict,
            and will not go deeper into it to search for "title" and "description", since they are a subset of "caseData".

        Returns:
            str: the JSON-string and the underlying levels recursively built
        """

        if path is None:
            path = []
        if result_obj is None:
            result_obj = {}

        for key, value in data.items():
            if filter.__contains__(key) or path.__contains__(filter):
                extended_path = self.extend_path(key, path)
                self.add_primitive_value(result_obj, '<br>', extended_path, value, 50)
                path.remove(key)

            elif isinstance(value, dict) or isinstance(value, list):
                extended_path = self.extend_path(key, path)
                if isinstance(value, dict):
                    exec(f'result_obj{extended_path} = {{}}')
                    self.dict_builder(value, filter, result_obj, path)

                elif isinstance(value, list):
                    exec(f'result_obj{extended_path} = []')
                    self.list_builder(value, filter, result_obj, path)

                self.check_for_empty_object(key, extended_path, result_obj, path)

        return result_obj

    def list_builder(self, data: list, filter: list, result_obj: object = None, path: list = None):
        """
        1 of 2 algorithms to recursively generate a JSON-structure, which is filtered by the provided filters given upon
        activation of this module in Cortex.

        Args:
            data (dict): new node of values, which can contain either a new node(list or dict) or a leaf (primitive type)
            filter: (list): target list of values which the new JSON-should contain
            result_obj: the new JSON-object, which holds the current progress of the algorithm
            path: used to keep track of the depth of the new JSON-object, to maintain the original object-structure

        Examples:
            FILTER_CANDIDATES = ["caseData", "title", "description"] - This takes all the data from caseData dict,
            and will not go deeper into it to search for "title" and "description", since they are a subset of "caseData".

        Returns:
            str: the JSON-string and the underlying levels built recursively.
        """
        if path is None:
            path = []
        if result_obj is None:
            result_obj = {}

        for value in data:
            if filter.__contains__(value) or path.__contains__(filter):
                key_chain = self.build_path(path)
                self.add_primitive_value(result_obj, '<br>', key_chain, value, 50)

            else:
                if isinstance(value, dict):
                    exec(f'result_obj{self.build_path(path)}.append({{}})')
                elif isinstance(value, list):
                    exec(f'result_obj{self.build_path(path)}.append([])')

                base_list = f'result_obj{self.build_path(path)}'
                base_index = eval(f'len({base_list}) - 1')
                extended_path = self.extend_path(base_index, path)

                if isinstance(value, dict):
                    self.dict_builder(value, filter, result_obj, path)
                elif isinstance(value, list):
                    self.list_builder(value, filter, result_obj, path)

                self.check_for_empty_object(base_index, extended_path, result_obj, path)

        return result_obj

    def extend_path(self, key, path: list):
        """
        adds another level to the tree-like JSON-object
        Args:
            key: name of the new node to be added.
            path: previous nodes, to enable chained index-operators.

        Returns:
            list: expanded list, representing the addition of an additional level.
        """
        path.append(key)
        return self.build_path(path)

    def add_primitive_value(self, result_obj, string_separator: str, extended_path: str, value, string_width=64):
        """
        Adds a new leaf-type value to the JSON-tree structure.
        Checks for long strings, and adds separator to them.

        Args:
            string_width:
            string_separator:
            extended_path:
            value:

        """
        if len(str(value)) > string_width and isinstance(value, str):
            formatted_value = self.insert(string_separator, value, string_width)
            exec(f"result_obj{extended_path} = \'{formatted_value}\'")
        else:
            exec(f"result_obj{extended_path} = value")

    @staticmethod
    def build_path(path: list):
        """
        Builds a chain of index operators, based on the elements in the provided path list.
        Args:
            path: list of index values.

        Returns:
            str: stringified chain of index operators
        """

        eval_string = ""
        for element in path:
            if isinstance(element, int):
                eval_string += f"[{element}]"
            else:
                eval_string += f"[\'{element}\']"

        return eval_string

    @staticmethod
    def insert(separator, string, line_width=64):
        """
             Helpermethod used to format strings of text.

             Args:
                 separator: operator to insert into text.
                 string: the text to add the elements to.
                 line_width: insert after how many characters.

             Returns:
                 str: formatted strings with the added elements in every interval.
             """
        words = iter(string.split())
        lines = []
        current = next(words)

        for word in words:
            if len(current) + 1 + len(word) > line_width:
                lines.append(current)
                current = word
            else:
                current += " " + word
                temp = len(current)

        lines.append(current)
        result = separator.join(lines)
        return result

    @staticmethod
    def check_for_empty_object(key, key_chain: list, result_obj: object, path: list):
        """
        Helpermethod for cleaning up empty objects in current level.

        Args:
            key: current tail element of the kay-chain to be removed.
            key_chain: generated chain of index brackets.
            result_obj: current build of JSON-object.
            path: current level in tree structure.
        """

        if len(eval(f'result_obj{key_chain}')) == 0:
            exec(f'del result_obj{key_chain}')
        path.remove(key)

    def send_mail(self, report_name, report_body):
        """
        Sends a mail with the generated HTML-page, which acts as a report over the case and the observables and tasks.
        Args:
            report_body:
            report_name:

        """

        mail_to = None
        if self.data_type == 'thehive:case':
            # Search recipient address in tags
            tags = self.get_param('data.tags', None, 'recipient address not found in tags')
            mail_tags = [t[5:] for t in tags if t.startswith('mail:')]
            if mail_tags:
                mail_to = mail_tags.pop()
            else:
                self.error('recipient address not found in observables')
        elif self.data_type == 'thehive:alert':
            # Search recipient address in artifacts
            artifacts = self.get_param('data.artifacts', None, 'recipient address not found in observables')
            mail_artifacts = [a['data'] for a in artifacts if a.get('dataType') == 'mail' and 'data' in a]
            if mail_artifacts:
                mail_to = mail_artifacts.pop()
            else:
                self.error('recipient address not found in observables')
        else:
            self.error('Invalid dataType')

        msg = EmailMessage()
        msg['Subject'] = f'Conscia Incident and Response - Case# {self.get_param("data.caseId", None, "Missing case")}'
        msg['From'] = self.mail_from
        msg['To'] = mail_to
        msg.set_content('Case Report')

        msg.add_attachment(report_body, subtype='html', filename=f'{report_name}.html')

        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as smtp:
            smtp.send_message(msg)

        self.report({'message': 'message sent'})

    def operations(self, raw):
        return [self.build_operation('AddTagToCase', tag='mail sent')]

    def run(self):
        Responder.run(self)

        case_id = self.get_param("data._id")
        filtered = self.dict_builder(self.get_case_data(case_id), self.case_data_filter)
        filtered.update(self.dict_builder(self.get_case_observables(case_id),
                                          self.case_observables_filter))
        filtered.update(self.dict_builder(self.get_case_tasks(case_id), self.case_tasks_filter))

        with open("templates/report_template_plus_jinja.html", "r") as file:
            html_template = file.read()

        template = Template(html_template)
        html_report = template.render(data=filtered["caseData"], observables=filtered["caseObservables"],
                                      tasks=filtered["caseTasks"])

        self.send_mail("test_case", html_report)


if __name__ == '__main__':
    Reporter().run()