from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
import re
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="个人记账API", description="支持自然语言输入的个人记账系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_natural_language(text: str) -> schemas.TransactionCreate:
    """解析自然语言输入"""
    # 匹配金额
    amount_pattern = r'\d+(\.\d+)?'
    amount_match = re.search(amount_pattern, text)
    if not amount_match:
        raise HTTPException(status_code=400, detail="无法识别金额")
    amount = float(amount_match.group())
    
    # 判断类型
    if any(word in text for word in ['收入', '收到', '工资', '报销']):
        transaction_type = schemas.TransactionType.INCOME
    else:
        transaction_type = schemas.TransactionType.EXPENSE
    
    # 清理描述文本
    description = text.strip()
    
    return schemas.TransactionCreate(
        amount=amount,
        type=transaction_type,
        description=description
    )

@app.post("/transactions/natural", response_model=schemas.Transaction)
def create_transaction_from_natural_language(
    input: schemas.NaturalLanguageInput,
    db: Session = Depends(get_db)
):
    """通过自然语言创建交易记录"""
    try:
        transaction_data = parse_natural_language(input.text)
        return crud.create_transaction(db=db, transaction=transaction_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    """创建交易记录"""
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取交易记录列表"""
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """获取单个交易记录"""
    db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="交易记录未找到")
    return db_transaction

@app.delete("/transactions/{transaction_id}", response_model=schemas.Transaction)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """删除交易记录"""
    db_transaction = crud.delete_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="交易记录未找到")
    return db_transaction

@app.get("/statistics/")
def get_statistics(days: int = 30, db: Session = Depends(get_db)):
    """获取统计信息"""
    return crud.get_statistics(db, days=days)