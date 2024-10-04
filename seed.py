from faker import Faker
from app import create_app, db
from models import User, Link, Vote, Comment
import random

fake = Faker()

ANCIENT_HISTORY_TOPICS = [
    "Ancient Egypt", "Roman Empire", "Greek Civilization", "Mesopotamia",
    "Indus Valley Civilization", "Ancient China", "Mayan Civilization",
    "Inca Empire", "Aztec Empire", "Persian Empire", "Carthaginian Empire", "Phoenician Civilization",
    "Babylonian Empire", "Assyrian Empire", "Hittite Empire", "Minoan Civilization",
    "Mycenaean Greece", "Sumerian Civilization", "Akkadian Empire", "Ancient Nubia",
    "Etruscan Civilization", "Scythian Culture", "Olmec Civilization", "Zapotec Civilization",
    "Parthian Empire", "Kushite Kingdom", "Nabataean Kingdom", "Xiongnu Confederation",
    "Gupta Empire", "Maurya Empire", "Qin Dynasty", "Han Dynasty"
]

ANCIENT_HISTORY_PHRASES = [
    "New archaeological discoveries in", "Unveiling the mysteries of",
    "Technological advancements of", "Political intrigue in",
    "Religious practices of", "Architectural wonders of",
    "Trade networks of", "Military strategies of",
    "Cultural exchanges between", "Ancient texts reveal secrets of",
    "Forgotten heroes of", "Environmental impact on",
    "Artistic achievements of", "Scientific knowledge in",
    "Women's roles in", "Childhood and education in",
    "Maritime explorations of", "Agricultural innovations in",
    "Linguistic developments in", "Mythological beliefs of",
    "Astronomical observations by", "Medical practices in",
    "Culinary traditions of", "Fashion and clothing in",
    "Sports and games in", "Musical instruments of",
    "Burial customs of", "Weaponry and warfare in",
    "Royal dynasties of", "Legal systems in"
]

def generate_ancient_history_title():
    topic = random.choice(ANCIENT_HISTORY_TOPICS)
    phrase = random.choice(ANCIENT_HISTORY_PHRASES)
    return f"{phrase} {topic}"

def generate_ancient_history_url():
    base_domains = ["ancienthistorytoday.com", "archaeologydaily.net", "historicalfindings.org", "pastcivilizations.info"]
    topic = random.choice(ANCIENT_HISTORY_TOPICS).lower().replace(" ", "-")
    return f"https://www.{random.choice(base_domains)}/{topic}/{fake.slug()}"

def seed_database():
    # Clear existing data
    db.session.query(Vote).delete()
    db.session.query(Comment).delete()
    db.session.query(Link).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create 10 users
    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.set_password(fake.password())
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Create 100 links
    links = []
    for _ in range(100):
        link = Link(
            title=generate_ancient_history_title(),
            url=generate_ancient_history_url(),
            user=random.choice(users)
        )
        links.append(link)
        db.session.add(link)
    db.session.commit()

    # Create 200 votes
    for _ in range(200):
        link = random.choice(links)
        user = random.choice(users)
        existing_vote = Vote.query.filter_by(user_id=user.id, link_id=link.id).first()
        if not existing_vote:
            vote = Vote(user=user, link=link)
            db.session.add(vote)
            link.score += 1
    db.session.commit()

    # Create 300 comments (some as replies)
    for _ in range(300):
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
