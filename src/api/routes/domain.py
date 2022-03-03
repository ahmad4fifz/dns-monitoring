from api.core.engine import dnx
from api.database.mongo import (
    #    add_domain,
    delete_domain,  # update_domain,
    retrieve_domain,
    #    retrieve_domains,
)
from api.models.domain import DomainSchema, ErrorResponseModel, ResponseModel
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

# query domain instantly
@router.get("/", response_description="Domain sent to engine for processing")
async def get_domains(domain: str):
    domains = dnx(domain)
    return domains  # by default, FastAPI will return data in JSON format


# @router.get("/", response_description="domains retrieved")
# async def get_domains():
#    domains = await retrieve_domains()
#    if domains:
#        return ResponseModel(domains, "domains data retrieved successfully")
#    return ResponseModel(domains, "Empty list returned")


# @router.post("/", response_description="domain added into the database")
# async def add_domain_data(domain: DomainSchema = Body(...)):
#    domain = jsonable_encoder(domain)
#    output_domain = await add_domain(domain)
#    return ResponseModel(output_domain, "domain processed.")


# async def add_domain_data(domain: DomainSchema = Body(...)):
#    domain = jsonable_encoder(domain)
#    new_domain = await add_domain(domain)
#    return ResponseModel(new_domain, "domain added successfully.")


@router.get("/{query}", response_description="domain data retrieved")
async def get_domain_data(query):
    domain = await retrieve_domain(query)
    if domain:
        return ResponseModel(domain, "domain data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "domain doesn't exist.")


# query domain, store in db, scheduler (add option to select schedule or not) schedule every 6h

# retrieve domain from database -> user input

# delete domain from database
@router.delete("/{query}", response_description="domain data deleted from the database")
async def delete_domain_data(query: str):
    deleted_domain = await delete_domain(query)
    if deleted_domain:
        return ResponseModel(
            "domain with query: {} removed".format(query), "domain deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "domain with query {0} doesn't exist".format(query)
    )
