from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.task import Task, TaskCreate, TaskUpdate
from app.auth.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# POST /tasks (requires authentication)
@router.post("/", status_code=201, dependencies=[Depends(get_current_user)])
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Task).where(func.lower(Task.title) == task.title.lower())
        )
        existing_task = result.scalars().first()

        if existing_task:
            raise HTTPException(
                status_code=400,
                detail=f"The title '{task.title}' is already used. Please try another one"
            )

        new_task = Task(title=task.title, description=task.description)
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)

        return {
            "message": "Task stored",
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")


# GET /tasks gets all tasks
@router.get("/")
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Task))
        tasks = result.scalars().all()

        return {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description
                }
                for task in tasks
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")


# GET /tasks/{task_id}
@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        task = await db.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")


# PUT /tasks/{task_id} update a task (requires authentication)
@router.put("/{task_id}", dependencies=[Depends(get_current_user)])
async def update_task(task_id: int, task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        task = await db.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = task_data.title
        task.description = task_data.description

        await db.commit()
        await db.refresh(task)

        return {
            "message": "Task updated",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")


# DELETE /tasks/{task_id} delete a task (requires authentication)
@router.delete("/{task_id}", dependencies=[Depends(get_current_user)])
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        task = await db.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        await db.delete(task)
        await db.commit()

        return {"message": "Task deleted"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")


# PATCH /tasks/{task_id} update a task title, description, or both (title cannot be empty)
@router.patch("/{task_id}", dependencies=[Depends(get_current_user)])
async def partial_update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    try:
        task = await db.get(Task, task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        # Check for duplicate title if updating title
        if task_data.title is not None:
            result = await db.execute(
                select(Task).where(func.lower(Task.title) ==
                                   task_data.title.lower(), Task.id != task_id)
            )
            existing_task = result.scalars().first()
            if existing_task:
                raise HTTPException(
                    status_code=400,
                    detail=f"The title '{task_data.title}' is already used. Please try another one"
                )
            task.title = task_data.title

        if task_data.description is not None:
            task.description = task_data.description

        await db.commit()
        await db.refresh(task)

        return {
            "message": "Task updated",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")
