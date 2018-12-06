import random
from faker import Faker
fake = Faker()

insertUser = ""
insertPost = ""
insertComment = ""
insertLike = ""
likes = []

for i in range(100):
    name = fake.name()
    email = fake.email()
    password_hash = name
    token = name
    is_admin = 0
    avatar_id = random.randint(0,10)

    insertSingleUser = ("INSERT INTO user (name, email, password_hash, token, is_admin, avatar_id) " + 
    f"VALUES ('{name}', '{email}', '{password_hash}', '{token}', {is_admin}, {avatar_id});\n") 

    insertUser += insertSingleUser

for i in range(100):
    poster_id = random.randint(1,100)
    category_id = random.randint(1,4)
    title = fake.sentence()
    content = fake.paragraph()
    post_time = fake.date() + " " + fake.time()

    insertSinglePost = ("INSERT INTO post (poster_id, category_id, title, content, post_time) " + 
    f"VALUES ({poster_id}, {category_id}, '{title}', '{content}', '{post_time}');\n")

    insertPost += insertSinglePost
  
for i in range(100):
    commenter_id = random.randint(1,100)
    post_id = random.randint(1, 100)
    content = fake.paragraph()
    post_time = fake.date() + " " + fake.time()

    insertSingleComment = ("INSERT INTO comment (commenter_id, post_id, content, post_time) " + 
    f"VALUES ({commenter_id}, {post_id}, '{content}', '{post_time}');\n")

    insertComment += insertSingleComment

  
for i in range(300):
    user_id = random.randint(1,100)
    post_id = random.randint(1, 100)

    insertSingleLike = ("INSERT INTO likes (user_id, post_id) " + 
    f"VALUES ({user_id}, {post_id});\n")

    if (user_id, post_id) in likes:
      continue

    likes.append((user_id,post_id))

    insertLike += insertSingleLike
  
finalSQL = insertUser + insertPost + insertComment + insertLike

f = open("initial.sql", "w")
f.write(finalSQL)
f.close()
