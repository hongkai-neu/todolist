'''
TODO Item model
'''

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TodoItem(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "priority": 1,
                "completed": False
            }
        }
    )

    id: Optional[int] = None
    title: str
    priority: int
    created_at: datetime = datetime.now()
    completed: bool = False 