from db.models import *
from db.database import *

from random import randint, choice
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for _ in range(length))

def generate_dummy_data():
    init_db()

    industries = list(Industry)
    with DBSessionContext(engine) as db:
        MAX = 10000
        MAX_REVIEWS = 24
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

            account = Account(username=f'account_{i}')
            account.add_password('account_i')
            objs.append(account)

            start_range = (i - 1) * 20
            end_range = ((i - 1) * 20) + 20
            for j in range(start_range, end_range):
                objs.append(Position(
                    name=f'position_{j}',
                    org_id=i
                ))

            for z in range(1, MAX_REVIEWS):
                objs.append(Review(
                    position_id=randint(start_range, end_range),
                    salary=randint(25000, 150000),
                    currency=Currency.GBP,
                    duration_years=z / 5,
                    post=f'This is review number: {z}.',
                    location='NY, USA',
                    account_id=randint(1, MAX - 1),
                    org_id=i,
                    tag=ReviewTag.GOOD if randint(0, 1) == 1 else ReviewTag.BAD
                    ))

                objs.append(Interview(
                    position_id=randint(start_range, end_range),
                    post=f'This is interview number: {z}.',
                    location='San Francisco, CA, USA',
                    offer=randint(25000, 150000),
                    currency=Currency.GBP,
                    account_id=randint(1, MAX - 1),
                    org_id=i,
                    tag=ReviewTag.GOOD if randint(0, 1) == 1 else ReviewTag.BAD
                    ))

        print("creating reviews and interviews votes\n")
        for i in range(1, 500000):
            objs.append(ReviewVote(
                account_id=randint(1, MAX - 1),
                review_id=randint(1, MAX * MAX_REVIEWS),
                vote=Vote.DOWNVOTE.value if randint(0, 1) == 1 else Vote.UPVOTE.value))
            objs.append(InterviewVote(
                account_id=randint(1, MAX - 1),
                interview_id=randint(1, MAX * MAX_REVIEWS),
                vote=Vote.DOWNVOTE.value if randint(0, 1) == 1 else Vote.UPVOTE.value))

        print(f"committing {len(objs)} rows\n")
        db.session.add_all(objs)
        db.session.commit()
