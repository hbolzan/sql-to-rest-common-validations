# Django SQL To REST Common Validations Service
This is part of Django SQL To Rest microservices ecosystem. 
This service provides validations to common forms data 
and it follows Django SQL To REST microservices guidelines.


## Requirements

RabbitMQ service must be running.


## How to install and run

Install
```
pip install -r requirements.txt
```

Run
```
nameko run services
```

## Service calls
This service accepts an RPC over AMQP call to service `common_validations`

## Validation Methods

### CPF
Validates CPF number. Possible responses are:


Method: `cpf`

Params: `value`

Error response
```
{
    "status": 400,
    "data": {
        "messages": {
            "en": "Invalid CPF number", 
            "pt-br": "Número de CPF inválido"
        },
        "additional_information": {
            "document": "<requested_cpf_number>",
            "valid_document": "<requested_cpf_with_correct_checksum_digits>"
        }
    }
}
```

Valid CPF

```
{
    "status": 200,
    "data": {
        "messages": {
            "en": "Valid CPF number", 
            "pt-br": "Número válido de CPF"
        },
        "additional_information": {
            "document": "<requested_cpf_number>",
            "subject_data": {
                # dict with additional data about the subject
                # in the case of CPF it could be
                "name": "If there is a name by CPF service available"
            }
        }
    }
}
```
