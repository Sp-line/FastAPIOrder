from __future__ import annotations

from typing import TYPE_CHECKING

from taskiq import ScheduleSource

if TYPE_CHECKING:
    from typing import Any
    from datetime import datetime
    from taskiq import AsyncTaskiqDecoratedTask


class TaskScheduler:
    def __init__(self, source: ScheduleSource) -> None:
        self._source = source

    async def schedule_by_time[**P](
            self,
            task: AsyncTaskiqDecoratedTask[P, Any],
            expires_at: datetime,
            schedule_id: str | None = None,
            *args: P.args,
            **kwargs: P.kwargs,
    ) -> None:
        if schedule_id:
            await (
                task
                .kicker()
                .with_schedule_id(schedule_id)
                .schedule_by_time(
                    self._source,
                    expires_at,
                    *args,
                    **kwargs
                )
            )
        else:
            await (
                task.schedule_by_time(
                    self._source,
                    expires_at,
                    *args,
                    **kwargs
                )
            )

    async def cancel_schedule(self, schedule_id: str) -> None:
        await self._source.delete_schedule(schedule_id)
