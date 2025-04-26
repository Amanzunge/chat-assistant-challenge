from typing import Literal, List

import dspy
from pydantic import BaseModel


class BaseAgent( dspy.Module ):
    def __init__( self, client, scratchpad ):
        super().__init__()
        self.client = client
        self.scratchpad = scratchpad


class ScratchpadEntry(BaseModel):
    entry_type: str
    entry_data: dict | list


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


class Message( BaseModel ):
    role: Literal['system', 'assistant', 'user', 'tool', 'scratchpad']
    content: str
    scratchpad: ScratchpadEntry | None = None


class History( BaseModel ):
    conversation: List[ Message ]

    def handle_message( self, message: Message ):
        self.conversation.append( message )

    def handle_tool_response( self, message: ToolResponse ):
        message = Message(
            role = 'tool',
            content = message.user_message + message.tool_response
        )
        self.handle_message( message )

        if message.scratchpad is not None:
            message = Message(
                role = 'scratchpad',
                content = '',
                scratchpad = message.scratchpad
            )
            self.handle_message( message )

    def format_history( self ):
        # :TODO: conversation should flow directly into dspy module. Not formatted as is.
        outputs = ''
        for entry in self.conversation:
            outputs += f'<|im_start|>{entry["role"]}: {entry["content"]}<|im_end|>'

        return outputs

    @property
    def text( self ):
        return self.format_history()
