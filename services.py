import requests
from nameko.rpc import rpc
from dstr_common_lib import responses
from dstr_common_lib.common_mixin import CommonMixin
from dstr_common_lib.util import clear_punctuation
from dstr_common_lib.consts import HTTP_STATUS_OK, HTTP_STATUS_ERROR
from dstr_common_lib.controller import handle_service_request
from logic import cnpj, cpf


DOC_TYPE_CPF = "CPF"
DOC_TYPE_CNPJ = "CNPJ"
VALIDATIONS = {
    DOC_TYPE_CPF: cpf,
    DOC_TYPE_CNPJ: cnpj,
}
NAME_BY_DOCUMENT_SERVICE = "name_by_document"

class CommonValidationsService(CommonMixin):
    name = "common_validations"

    def __init__(self):
        self.name_service_available = None

    @rpc
    def health_check(self):
        return self.common_health_check()

    @rpc
    def refresh(self):
        """
        refreshes name service check property,
        so if name service is started after check was done,
        it will be checked again in the next call to cpf or cnpj
        """
        self.name_service_available = None
        return responses.common(HTTP_STATUS_OK, {"en": "OK", "pt-br": "OK"})

    @rpc
    def cpf(self, cpf_number, with_name=False):
        return self.document_validate(DOC_TYPE_CPF, cpf_number, with_name)

    @rpc
    def cnpj(self, cnpj_number, with_name=False):
        return self.document_validate(DOC_TYPE_CNPJ, cnpj_number, with_name)

    def document_validate(self, document_type, document_number, with_name):
        valid, expected = VALIDATIONS[document_type].validate(document_number)
        if valid:
            subject_data = {}
            if with_name and self.check_name_service_available():
                name_info = handle_service_request(
                    NAME_BY_DOCUMENT_SERVICE,
                    "get_name",
                    document_type=document_type,
                    document_number=document_number
                )
                subject_data = name_info["body"]["data"].get("additional_information", {})
            return self.success(document_type, document_number, subject_data)
        return self.error(document_type, document_number, expected)

    def check_name_service_available(self):
        if self.name_service_available is None:
            h = handle_service_request(NAME_BY_DOCUMENT_SERVICE, "health_check")
            self.name_service_available = h.get("http_status") == 200
        return self.name_service_available

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
