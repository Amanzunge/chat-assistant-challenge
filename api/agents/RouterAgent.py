
from datetime import datetime

from api.agents.BaseAgent import BaseAgent


class RootRouterAgent( BaseAgent ):
    def __init__( self, *args ):
        super().__init__( *args )

    def forward( self, history, request, today = None ):
        if today is None:
            today = datetime.now().strftime( "%Y-%m-%d" )
        return {}
