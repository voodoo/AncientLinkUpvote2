from faker import Faker
from app import create_app, db
from models import User, Link, Vote, Comment
import random

fake = Faker()

def seed_database():
    # Clear existing data
    db.session.query(Vote).delete()
    db.session.query(Comment).delete()
    db.session.query(Link).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create 2 users
    users = []
    for _ in range(2):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.set_password(fake.password())
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Create 20 links
    links = []
    for _ in range(20):
        link = Link(
            title=fake.catch_phrase(),
            url=fake.url(),
            user=random.choice(users)
        )
        links.append(link)
        db.session.add(link)
    db.session.commit()

    # Create 40 votes
    for _ in range(40):
        vote = Vote(
            user=random.choice(users),
            link=random.choice(links)
        )
        db.session.add(vote)
        link.score += 1
    db.session.commit()

    # Create 50 comments (some as replies)
    for _ in range(50):
        parent = None
        if random.random() < 0.3 and Comment.query.count() > 0:
            parent = random.choice(Comment.query.all())
        
        comment = Comment(
            content=fake.paragraph(),
            user=random.choice(users),
            link=random.choice(links),
            parent=parent
        )
        db.session.add(comment)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()
