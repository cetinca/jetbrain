from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_name = "flashcard.db"
Base = declarative_base()
engine = create_engine(f"sqlite:///{database_name}?check_same_thread=False", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.question!r}, fullname={self.answer!r}, box={self.box!r})"

    @classmethod
    def find_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_box(cls, box_numbers):
        return session.query(cls).filter(cls.box.in_(box_numbers)).all()

    @staticmethod
    def add_flashcard(question, answer, box=1):
        flashcard = Flashcard(question=question, answer=answer, box=box)
        session.add(flashcard)
        session.commit()
        return flashcard

    @staticmethod
    def update_flashcard(card, question, answer):
        card.question = question
        card.answer = answer
        session.commit()

    @staticmethod
    def update_attr(card, **kwargs):
        for k, v in kwargs.items():
            setattr(card, k, v)
            session.commit()

    @staticmethod
    def delete_flashcard(card):
        session.delete(card)
        session.commit()


Base.metadata.create_all(engine)
