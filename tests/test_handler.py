from moto import mock_events
import boto3
from pydantic import BaseModel

from event_handler import EventHandler


class GenericModel(BaseModel):
    id: int
    generic_text: str


@mock_events
def test_event_handler():
    handler = EventHandler(
        "TAPI",
        prefix="test_prefix",
        region_name="eu-west-1",
        aws_access_key_id="generic_access_key_id",
        aws_secret_access_key="generic_access_key_key",
    )
    event = GenericModel(id=1, generic_text="this is a test")
    handler.send_event("com.pleaseignore.auth", event)
