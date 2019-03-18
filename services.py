import re
from nameko.rpc import rpc
from dstr_common_lib import responses
from dstr_common_lib.util import clear_punctuation
from logic import cnpj, cpf


class CommonValidationsService:
    name = "common_validations"

    @rpc
    def cpf(self, cpf_number):
        valid, expected = cpf.validate(cpf_number)
        if valid:
            return self.success(cpf_number)
        return self.error(cpf_number, expected)

    def success(self, cpf_number):
        return responses.common(
            "OK",
            {"en": "Valid CPF number", "pt-br": "Número válido de CPF"},
            {"cpf": cpf_number, "person_name": "",}
        )

    def error(self, cpf_number, expected_cpf):
        return responses.common(
            "ERROR",
            {"en": "Invalid CPF number", "pt-br": "Número de CPF inválido"},
            {"cpf": cpf_number, "valid_cpf": expected_cpf,}
        )
