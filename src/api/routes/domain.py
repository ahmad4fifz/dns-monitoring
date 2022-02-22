from time import time

from api.core.engine import SESSION_MAX, SESSION_TTL, THREADS, Session
from api.database import (
    add_domain,
    delete_domain,
    retrieve_domain,
    retrieve_domains,
#    update_domain,
)
from api.models.domain import (
    DomainSchema,
    ErrorResponseModel,
    ResponseModel,
)
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

router = APIRouter()
sessions = []


@router.post("/", response_description="domain added into the database")
async def add_domain_data(domain: DomainSchema = Body(...)):
    for s in sessions:
        status = s.status()
        if status["remaining"] == 0 and (status["timestamp"] + SESSION_TTL) < time():
            sessions.remove(s)
    if len(sessions) >= SESSION_MAX:
        return (
            ErrorResponseModel(
                "An error occurred.",
                500,
                "Too many scan sessions - please retry in a minute",
            ),
        )
    if "url" not in request.json:
        return (ErrorResponseModel("An error occurred.", 400, "Invalid request"),)
    for suburl in request.json["url"].split("."):
        if len(suburl) > 15:
            return (
                ErrorResponseModel(
                    "An error occurred.", 400, "Domain name is too long"
                ),
            )
    try:
        session = Session(request.json.get("url"))
    except Exception as err:
        return (ErrorResponseModel("An error occurred.", 400, "Invalid domain name"),)
    else:
        session.scan()
        sessions.append(session)
    return ResponseModel(session.status()), 201


# async def add_domain_data(domain: DomainSchema = Body(...)):
#    domain = jsonable_encoder(domain)
#    new_domain = await add_domain(domain)
#    return ResponseModel(new_domain, "domain added successfully.")


@router.get("/", response_description="domains retrieved")
async def get_domains():
    domains = await retrieve_domains()
    if domains:
        return ResponseModel(domains, "domains data retrieved successfully")
    return ResponseModel(domains, "Empty list returned")


@router.get("/{query}", response_description="domain data retrieved")
async def get_domain_data(query):
    domain = await retrieve_domain(query)
    if domain:
        return ResponseModel(domain, "domain data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "domain doesn't exist.")

# no UPDATE function

#@router.put("/{query}")
#async def update_domain_data(query: str, req: UpdateDomainModel = Body(...)):
#    req = {k: v for k, v in req.dict().items() if v is not None}
#    updated_domain = await update_domain(query, req)
#    if updated_domain:
#        return ResponseModel(
#            "domain with query: {} name update is successful".format(query),
#            "domain name updated successfully",
#        )
#    return ErrorResponseModel(
#        "An error occurred",
#        404,
#        "There was an error updating the domain data.",
#    )


# query domain instant (check in db 1st... if no record, query domain)

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
