# Django SQL To REST Common Validations Service
This is part of Django SQL To Rest microservices ecosystem. 
This service provides validations to common forms data 
and it follows Django SQL To REST microservices guidelines.


## Validations

### CPF
Validates CPF number. Possible responses are:


Endpoint:
```
/cpf/<cpf_number>
```

Error response
```
{
    "status": "ERROR",
    "data": {
        "messages": {"en": "Invalid CPF number", "pt-br": "Número de CPF inválido"},
        "additional_information": {
            "requested_cpf": "<requested_cpf_number>",
            "valid_cpf": "<requested_cpf_with_correct_checksum_digits>"
        }
    }
}
```

Valid CPF

```
{
    "status": "OK",
    "data": {
        "messages": {"en": "Valid CPF number", "pt-br": "Número válido de CPF"},
        "additional_information": {
            "cpf": "<requested_cpf_number>",
            "person_name": "Person name if there is an available person index service"
        }
    }
}
```
