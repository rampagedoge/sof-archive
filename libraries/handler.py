# this prevents shit from blowing up
# aka the mongodb handler that cosmos uses!??!? wtf??
import logging
import collections

class Document:
  def __init__(self, connection, document_name):
    #connects the thinger
    self.db = connection[document_name]
    self.logger = logging.getLogger(__name__)
  # Functions that point to the other function
  async def update(self, dict):
    await self.update_by_id(dict)
  async def get_by_id(self, id):
    return await self.find_by_id(id)
  async def find(self, id):
    return await self.find_by_id(id)
  async def delete(self, id):
    await self.delete_by_id(id)
  # Main functions
  async def find_by_id(self, id):
    return await self.db.find_one({"_id":id})
  async def find_by_val(self,key,val):
    return await self.db.find_one({key:val})
  async def update_dict(self, id, name, key, val):
    if not await self.find_by_id(id):
      await self.db.insert({"_id":id,name:{key:val}})
      return
    await self.db.update_one({"_id":id},{"$set":{f"{name}.{key}":val}})
  async def append_dict(self,id,name,key,val):
    if not await self.find_by_id(id): return
    data = await self.find_by_id(id)
    data[name][key] = val
    await self.upsert(data)
  async def append_list(self,id,name,val):
    if not await self.find_by_id(id): return
    data = await self.find_by_id(id)
    data[name].append(val)
    await self.upsert(data)
  async def pop_dict(self,id,name,key):
    if not await self.find_by_id(id): return
    data = await self.find_by_id(id)
    data[name].pop(key)
    await self.upsert(data)
  async def delete_by_id(self, id):
    if not await self.find_by_id(id): return
    await self.db.delete_many({"_id":id})
  async def insert(self, dict):
    if not isinstance(dict, collections.abc.Mapping):
      raise TypeError("Expected type Dictionary")
    if not dict["_id"]:
      raise KeyError("_id not found in given dict.")
    await self.db.insert_one(dict)
  async def upsert(self, dict):
    if await self.find(dict["_id"]) != None:
      await self.update_by_id(dict)
    else:
      await self.db.insert_one(dict)
  async def update_by_id(self, dict):
    if not isinstance(dict, collections.abc.Mapping):
      raise TypeError("Expected type Dictionary")
    if not dict["_id"]:
      raise KeyError("_id not found in given dict.")
    if not await self.find_by_id(dict["_id"]):
      return
    id = dict["_id"]
    dict.pop("_id")
    await self.db.update_one({"_id": id},{"$set":dict})
  async def unset(self, dict):
    if not isinstance(dict, collections.abc.Mapping):
      raise TypeError("Expected type Dictionary")
    if not dict["_id"]:
      raise KeyError("_id not found in given dict.")
    if not await self.find_by_id(dict["_id"]):
      return
    id = dict["_id"]
    dict.pop("_id")
    await self.db.update_one({"_id":id},{"$unset":dict})
  async def increment(self, id, amount, field):
    if not await self.find_by_id(id):
      return
    await self.db.update_one({"_id":id},{"$inc":{field:amount}})
  async def get_all(self):
    data = []
    async for document in self.db.find({}):
      data.append(document)
    return data