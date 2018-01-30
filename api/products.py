from flask_injector import inject
from providers.CouchProvider import CouchProvider


@inject(data_provider=CouchProvider)
def create_product(data_provider,productPayload) -> str:
    return data_provider.create_product(productPayload)

@inject(data_provider=CouchProvider)
def read_product(data_provider, prod_id) -> str:
    return data_provider.read_product(prod_id)

@inject(data_provider=CouchProvider)
def update_product(data_provider,productPayload) -> str:
    return data_provider.update_product(productPayload)

@inject(data_provider=CouchProvider)
def delete_product(data_provider,prod_id) -> str:
    return data_provider.delete_product(prod_id)