import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# ПОДКЛЮЧАЕМ БИБЛИОТЕКУ ДЛЯ МЕТРИК
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class TodoCreate(BaseModel):
    title: str

class TodoOut(TodoCreate):
    id: int
    completed: bool
    class Config:
        from_attributes = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- АВТОМАТИЧЕСКИЙ СБОР МЕТРИК ДЛЯ PROMETHEUS ---
# Этот блок создаст эндпоинт /metrics и начнет считать все входящие запросы
Instrumentator().instrument(app).expose(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items", response_model=List[TodoOut])
def read_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.post("/items", response_model=TodoOut)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/items/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/items/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Deleted"}
