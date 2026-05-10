"""Database utilities - write queue for SQLite concurrency"""
import asyncio
from typing import Callable, Awaitable, Any
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session_factory


@dataclass
class WriteJob:
    fn: Callable[[AsyncSession], Awaitable[Any]]
    future: asyncio.Future


_write_queue: asyncio.Queue[WriteJob] = asyncio.Queue()
_writer_task = None


async def _db_writer_loop():
    """Single worker that processes all DB writes sequentially"""
    factory = get_session_factory()
    while True:
        job = await _write_queue.get()
        try:
            async with factory() as session:
                try:
                    result = await job.fn(session)
                    await session.commit()
                    job.future.set_result(result)
                except Exception as e:
                    await session.rollback()
                    job.future.set_exception(e)
        except Exception as e:
            if not job.future.done():
                job.future.set_exception(e)


def start_db_writer():
    """Start the background DB writer"""
    global _writer_task
    loop = asyncio.get_running_loop()
    _writer_task = loop.create_task(_db_writer_loop())
    return _writer_task


def stop_db_writer():
    """Stop the background DB writer"""
    global _writer_task
    if _writer_task:
        _writer_task.cancel()
        _writer_task = None


async def write_to_db(fn: Callable[[AsyncSession], Awaitable[Any]], timeout: float = 30) -> Any:
    """Submit a write job to the queue and wait for result"""
    future = asyncio.get_running_loop().create_future()
    await _write_queue.put(WriteJob(fn=fn, future=future))
    return await asyncio.wait_for(future, timeout=timeout)
