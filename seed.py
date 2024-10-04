from faker import Faker
from app import create_app, db
from models import User, Link, Vote, Comment
import random

fake = Faker()

ANCIENT_HISTORY_TOPICS = [
    "Ancient Egypt", "Roman Empire", "Greek Civilization", "Mesopotamia",
    "Indus Valley Civilization", "Ancient China", "Mayan Civilization",
    "Inca Empire", "Aztec Empire", "Persia", "Carthage", "Phoenicia",
    "Babylon", "Assyria", "Hittite Empire", "Minoan Civilization",
    "Mycenaean Greece", "Sumer", "Akkadian Empire", "Ancient Nubia"
]

ANCIENT_HISTORY_PHRASES = [
    "Discoveries in", "New findings about", "The rise and fall of",
    "Uncovering secrets of", "Archaeological breakthroughs in",
    "The mysteries of", "Daily life in", "Warfare and politics in",
    "Art and culture of", "Religious practices in", "Trade routes of",
    "Technological advancements in", "The rulers of", "Monuments and architecture of",
    "Ancient texts reveal", "Myths and legends of", "The fall of",
    "Excavations uncover", "Historical analysis of", "Reconstructing"
]

def generate_ancient_history_title():
    topic = random.choice(ANCIENT_HISTORY_TOPICS)
    phrase = random.choice(ANCIENT_HISTORY_PHRASES)
    return f"{phrase} {topic}"

def generate_ancient_history_url():
    topic = random.choice(ANCIENT_HISTORY_TOPICS).lower().replace(" ", "-")
    return f"https://ancient-history-news.com/{topic}/{fake.slug()}"

def seed_database():
    # Clear existing data
    db.session.query(Vote).delete()
    db.session.query(Comment).delete()
    db.session.query(Link).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create 5 users
    users = []
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.set_password(fake.password())
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Create 50 links
    links = []
    for _ in range(50):
        link = Link(
            title=generate_ancient_history_title(),
            url=generate_ancient_history_url(),
            user=random.choice(users)
        )
        links.append(link)
        db.session.add(link)
    db.session.commit()

    # Create 100 votes
    for _ in range(100):
        vote = Vote(
            user=random.choice(users),
            link=random.choice(links)
        )
        db.session.add(vote)
        link.score += 1
    db.session.commit()

    # Create 200 comments (some as replies)
    for _ in range(200):
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
