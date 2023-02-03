from sqlalchemy import create_engine
from typing import TypeVar, Any
from sqlalchemy.orm import sessionmaker
from database.models import Post


Session = TypeVar('Session')


class Database:
    def __init__(self) -> None:
        db_uri = "sqlite:///db.db"
        self.engine = create_engine(db_uri)
        Post.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, obj: Session) -> None:
        self.session.add(obj)
        self.session.commit()

    def get(self, obj: Session, id: int) -> Any:
        return self.session


if __name__ == "__main__":
    import datetime
    db = Database()
    post = Post(title="Test", content="Test", release=datetime.datetime.now(), generated=datetime.datetime.now())
    # db.add(post)
    print(db.get(Post, 1))
