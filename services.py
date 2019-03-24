import requests
from nameko.rpc import rpc
from dstr_common_lib import responses
from dstr_common_lib.common_mixin import CommonMixin
from dstr_common_lib.util import clear_punctuation
from dstr_common_lib.consts import HTTP_STATUS_OK, HTTP_STATUS_ERROR
from logic import cnpj, cpf


DOC_TYPE_CPF = "CPF"
DOC_TYPE_CNPJ = "CNPJ"
VALIDATIONS = {
    DOC_TYPE_CPF: cpf,
    DOC_TYPE_CNPJ: cnpj,
}

class CommonValidationsService(CommonMixin):
    name = "common_validations"

    @rpc
    def health_check(self):
        return self.common_health_check()

    @rpc
    def cpf(self, cpf_number):
        return self.validate(DOC_TYPE_CPF, cpf_number)

    @rpc
    def cnpj(self, cnpj_number):
        return self.validate(DOC_TYPE_CNPJ, cnpj_number)

    def validate(self, document_type, document_number):
        valid, expected = VALIDATIONS[document_type].validate(document_number)
        if valid:
            return self.success(document_type, document_number)
        return self.error(document_type, document_number, expected)

    @rpc
    def cep(self, cep_number):
        r = requests.get("https://viacep.com.br/ws/{}/json/".format(cep_number))
        # TODO: fallback to local cache
        if r.status_code == 200:
            if r.json().get("erro"):
                return self.error("CEP", cep_number, None, 409)
            return self.success("CEP", cep_number, r.json())
        return self.error("CEP", cep_number, None, r.status_code)

    def success(self, document_type, document_number, subject_data={}):
        return responses.common(
            HTTP_STATUS_OK,
            {
                "en": "Valid {} number".format(document_type),
                "pt-br": "Número válido de {}".format(document_type)
            },
            {"document": document_number, "subject_data": subject_data,}
        )

    def error(self, document_type, document_number, expected_document=None, http_status=HTTP_STATUS_ERROR):
        return responses.common(
            http_status,
            {
                "en": "Invalid {} number".format(document_type),
                "pt-br": "Número de {} inválido".format(document_type)
            },
            {"document": document_number, "valid_document": expected_document,}
        )
