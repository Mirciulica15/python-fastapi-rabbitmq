from pydantic import BaseModel


class RequestObject(BaseModel):
    order_id: str
    action: str = None

    def add_action(self, action: str):
        self.action = action
        return self
