import json
from typing import List, Dict, Optional

from pydantic import BaseModel, ConfigDict, TypeAdapter

from api.humanity_client.client import Client


class ScratchpadEntry(BaseModel):
    entry_type: str
    entry_data: dict | list


class Employee(BaseModel):
    id: str
    name: str
    avatar: Optional[None | Dict | str ] = None

    def model_post_init(self, __context):
        if isinstance( self.avatar, str ):
            self.avatar = json.loads( self.avatar )
            for avatar_size in self.avatar.keys():
                if self.avatar[avatar_size].startswith( 'https://www.humanity.com/'):
                    continue
                else:
                    self.avatar[ avatar_size ] = f'https://www.humanity.com/{self.avatar[ avatar_size ]}'


class Time(BaseModel):
    date: str
    time: str
    formatted: str


class Shift(BaseModel):
    model_config = ConfigDict( extra = 'ignore' )

    id: int
    title: str
    schedule: int
    schedule_name: str
    employees: List[ Employee ]
    start_date: Time
    end_date: Time


class ToolResponse(BaseModel):
    """
    user_message: message to display directly to the user.
    tool_response: data to present to the language model, usually json.
    scratchpad: A scratchpad entry that can be rendered for the user
    """
    user_message: str = ''
    tool_response: str = ''
    scratchpad: ScratchpadEntry | None = None
    return_to_client: bool = False


CLIENT_TYPE = Client
SCRATCHPAD_TYPE = List[ScratchpadEntry]


async def load_shifts(
    start_date: str,
    stop_date: str,
    client: CLIENT_TYPE,
    scratchpad: SCRATCHPAD_TYPE
) -> ToolResponse:
    # :TODO:
    ...