import uuid

# в данном случае значение будет изменяться
# USER_ACTIVATION_NAMESPACE = uuid.uuid4()

# если необходимо привязаться, то нужно указать сгенерированный uuid (берем в инете)  #noqa
USER_ACTIVATION_UUID_NAMESPACE = uuid.UUID(
    "966f45c6-5b7b-47fc-9d13-7ed676a3b322"
)  # noqa
