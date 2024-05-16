"""
把formulamodelstruct表中所有包含检测结果的配方单创建项目
"""
import asyncio
import pandas as pd
import uuid

from app.utils.database import engine as sql_engine
from app.models import repos_orms
from app.utils.database import insert_many, async_session


async def async_main():
    async with sql_engine.begin() as conn:
        await conn.run_sync(repos_orms.Base.metadata.create_all)

        df = pd.read_csv("Properties.csv")

    properties = []
    for _, row in df.iterrows():
        property = repos_orms.Properties(Id = str(uuid.uuid4()), **{k: v for k, v in row.items() if k in vars(repos_orms.Properties)})
        properties.append(property)
        properties.append(property)
    await insert_many(async_session, properties)
        
asyncio.run(async_main())