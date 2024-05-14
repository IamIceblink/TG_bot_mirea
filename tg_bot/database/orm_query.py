from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


from database.models import Task, User, Group



async def set_user(session: AsyncSession, tg_id) -> bool:
    user = await session.scalar(select(User).where(User.tg_id==tg_id))
    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()
        return False
    else:
        return True
    

#-------------------------------------------------------------------------
    

async def orm_add_group(session: AsyncSession, data: dict):
    obj = Group(
        name = data["newgroup"],
    )
    session.add(obj)
    await session.commit()

    
#-------------------------------------------------------------------------


async def orm_add_task(session: AsyncSession, data: dict):
    obj = Task(
        group = data["group"],
        name = data["name"],
        date = data["date"],
        is_done = False,
    )
    session.add(obj)
    await session.commit()


async def orm_get_tasks(session: AsyncSession):
    query = select(Task)
    #.where(Task.uid == uid)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_edit_task(session: AsyncSession, task_id: int, data: dict):
    query = update(Task).where(Task.id == task_id).values(
        group = data["group"],
        name = data["name"],
        date = data["date"],
        is_done = False,
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_task(session: AsyncSession, task_id: int):
    query = delete(Task).where(Task.id == task_id)
    await session.execute(query)
    await session.commit()


#---------------------------------------------------------------------------------


async def orm_your_name(session: AsyncSession, tg_id: int, data: dict):
    query = update(User).where(User.tg_id == tg_id).values(
        name = data["your_name"],
    )
    await session.execute(query)
    await session.commit()


async def orm_change_your_name(session: AsyncSession, tg_id: int, data: dict):
    query = update(User).where(User.tg_id == tg_id).values(
        name = data["acceptance"],
    )
    await session.execute(query)
    await session.commit()


async def orm_get_name(session: AsyncSession, tg_id: int) -> str:
    query = select(User.name).where(User.tg_id==tg_id)
    result = await session.execute(query)
    return result.scalar()


#----------------------------------------------------------------------------------
    



