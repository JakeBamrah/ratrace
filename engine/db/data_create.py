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
                id=i,
                name=f'org_{randomword(randint(3, 15))}_{i}',
                size=randint(1, 5000),
                headquarters="London, UK",
                industry=industries[randint(0, 21)],
                page_visits=randint(0, 5000),
                url=f'www.org_{i}_website.com'
                ))
            objs.append(Account(username=f'account_{i}'))

            for j in range(1, 20):
                objs.append(Position(
                    name=f'position_{j}',
                    org_id=i
                ))

        print("creating reviews and interviews\n")
        for i in range(1, 200000):
            objs.append(Review(
                position_id=randint(1, 100000),
                salary=randint(25000, 150000),
                currency=Currency.GBP,
                duration_years=i / 5,
                review=f'This is review number: {i}.',
                location='NY, USA',
                account_id=randint(1, MAX - 1),
                org_id=randint(1, MAX - 1),
                tag=ReviewTag.GOOD if randint(0, 1) == 1 else ReviewTag.BAD
                ))

            objs.append(Interview(
                position_id=randint(1, 100000),
                interview=f'This is interview number: {i}.',
                location='San Francisco, CA, USA',
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
                vote=Vote.DOWNVOTE.value if randint(0, 1) == 1 else Vote.UPVOTE.value))
            objs.append(InterviewVote(
                account_id=randint(1, MAX - 1),
                interview_id=randint(1, 200000 - 1),
                vote=Vote.DOWNVOTE.value if randint(0, 1) == 1 else Vote.UPVOTE.value))

        print(f"committing {len(objs)} rows\n")
        db.session.add_all(objs)
        db.session.commit()
