from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import desc

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None
):
    query = db.query(models.Transaction)
    
    if start_date:
        query = query.filter(models.Transaction.created_at >= start_date)
    if end_date:
        query = query.filter(models.Transaction.created_at <= end_date)
    
    return query.order_by(desc(models.Transaction.created_at)).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
    return transaction

def get_statistics(db: Session, days: int = 30):
    """获取统计信息"""
    start_date = datetime.now() - timedelta(days=days)
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.created_at >= start_date
    ).all()
    
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_amount": total_income - total_expense,
        "period_days": days
    }