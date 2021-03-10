import boto3
from pydantic import BaseModel
from typing import List


class EventHandler:
    def __init__(self, event_bus: str, *, prefix: str = None, **boto_opts):
        self.event_bus: str = event_bus
        self.session = boto3.Session(**boto_opts)
        self.prefix = prefix

    def send_event(
        self,
        sender: str,
        event: BaseModel,
        extra_resources: List[str] = [],
        detail_type: str = None,
        event_bus: str = None,
    ) -> dict:
        event_bus = self.event_bus if not event_bus else event_bus
        event = dict(
            Source=sender,
            Detail=event.json(),
            Resources=extra_resources,
            DetailType=f"{event_bus}:{self.prefix}",
            EventBusName=event_bus,
        )
        send_event = self.session.client("events").put_events(
            Entries=[
                event,
            ]
        )

        if not send_event.get("FailedEntryCount") == 0:
            raise Exception(
                f"{send_event.get('Entries')[0].get('ErrorCode')}: {send_event.get('Entries')[0].get('ErrorMessage')}"
            )

        return send_event
