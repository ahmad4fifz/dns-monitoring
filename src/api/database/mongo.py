import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.domains

domain_collection = database.get_collection("domains_collection")

# helpers
def domain_helper(domain) -> dict:
    return {
        "fuzzer": domain["fuzzer"],
        "domain": domain["domain"],
        "dns_a": domain["dns_a"],
        "dns_aaaa": domain["dns_aaaa"],
        "dns_mx": domain["dns_mx"],
        "geoip": domain["geoip"],
    }


# Retrieve all domains present in the database
async def retrieve_domains():
    domains = []
    async for domain in domain_collection.find():
        domains.append(domain_helper(domain))
    return domains


# Add a new domain into to the database
async def add_domain(domain_data: dict) -> dict:
    domain = await domain_collection.insert_one(domain_data)
    new_domain = await domain_collection.find_one({"_id": domain.inserted_id})
    return domain_helper(new_domain)


# Retrieve a domain with a matching ID
async def retrieve_domain(id: str) -> dict:
    domain = await domain_collection.find_one({"_id": ObjectId(id)})
    if domain:
        return domain_helper(domain)


# Update a domain with a matching ID
#async def update_domain(id: str, data: dict):
#    # Return false if an empty request body is sent.
#    if len(data) < 1:
#        return False
#    domain = await domain_collection.find_one({"_id": ObjectId(id)})
#    if domain:
#        updated_domain = await domain_collection.update_one(
#            {"_id": ObjectId(id)}, {"$set": data}
#        )
#        if updated_domain:
#            return True
#        return False


# Delete a domain from the database
async def delete_domain(id: str):
    domain = await domain_collection.find_one({"_id": ObjectId(id)})
    if domain:
        await domain_collection.delete_one({"_id": ObjectId(id)})
        return True
