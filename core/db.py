from motor.motor_asyncio import AsyncIOMotorClient
from umongo import MotorAsyncIOInstance

import settings


class MongoInstance(MotorAsyncIOInstance):

    async def init(self, db):
        super().init(db)
        for model in self._doc_lookup.values():
            await model.ensure_indexes()

mongo_instance = MongoInstance()


async def init_db(app):
    app.client = AsyncIOMotorClient(settings.MONGO_HOST)
    app.db = app.client[settings.MONGO_DB_NAME]

    # Init mongo models
    await mongo_instance.init(app.db)


async def close_db(app):
    app.client.close()


async def include_references(objects, reference_fields):
    for field in reference_fields:
        cached_reference_objects = {}
        for obj in objects:
            reference_field = getattr(obj, field)
            reference_field_pk = reference_field.pk
            if not reference_field_pk in cached_reference_objects:
                cached_reference_objects[reference_field_pk] = await reference_field.fetch()
            else:
                reference_field._document = cached_reference_objects[reference_field_pk]
