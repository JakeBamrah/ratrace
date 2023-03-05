from db.models import *
from db.database import *

from random import randint, choice
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))

def generate_dummy_data():
    init_db()

    industries = list(Industry)
    with DBSessionContext(engine) as db:
        MAX = 10000
        objs = []
        print("creating companies and accounts\n")
        for i in range(1, MAX):
            objs.append(Organisation(
                name=f'org_{randomword(randint(3, 15))}_{i}',
                size=randint(1, 5000),
                headquarters="London, UK",
                industry=industries[randint(0, 21)],
                page_visits=randint(0, 5000),
                times_visited=randint(0, 5000),
                url=f'www.org_{i}_website.com'
                ))
            objs.append(Account(username=f'account_{i}'))

        print("creating reviews and interviews\n")
        for i in range(1, 200000):
            objs.append(Review(
                position=f'review_{i}',
                salary=randint(25000, 150000),
                currency=Currency.GBP,
                duration_years=i / 5,
                review=f'This is review number: {i}.',
                location='NY',
                account_id=randint(1, MAX - 1),
                org_id=randint(1, MAX - 1),
                tag=ReviewTag.GOOD if randint(0, 1) == 1 else ReviewTag.BAD
                ))
            objs.append(Interview(
                position=f'interview_{i}',
                interview=f'This is interview number: {i}.',
                location='NY',
                offer=randint(25000, 150000),
                currency=Currency.GBP,
                account_id=randint(1, MAX - 1),
                org_id=randint(1, MAX - 1),
                tag=ReviewTag.GOOD if randint(0, 1) == 1 else ReviewTag.BAD
                ))
        print("creating reviews and interviews votes\n")
        for i in range(1, 500000):
            objs.append(ReviewVote(
                account_id=randint(1, MAX - 1),
                review_id=randint(1, 200000 - 1),
                vote=Vote.DOWNVOTE if randint(0, 1) == 1 else Vote.UPVOTE))
            objs.append(InterviewVote(
                account_id=randint(1, MAX - 1),
                interview_id=randint(1, 200000 - 1),
                vote=Vote.DOWNVOTE if randint(0, 1) == 1 else Vote.UPVOTE))

        print(f"committing {len(objs)} rows\n")
        db.session.add_all(objs)
        db.session.commit()
