from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="交易金额")
    type: TransactionType = Field(..., description="交易类型：收入或支出")
    description: str = Field(..., min_length=1, description="交易描述")

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NaturalLanguageInput(BaseModel):
    text: str = Field(..., min_length=1, description="自然语言输入，例如：'今天买菜花了50元'")