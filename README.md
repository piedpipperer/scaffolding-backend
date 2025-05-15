# relapmidos-backend

Things to consider to test the endpoint localy. once its a basis.


# have to make sure database is created (the one present in db connections)

# after, execute
poetry run python ./database/db_initialization.py

# idealy run the fastapi:
uvicorn tiny_relappmidos:app --reload
# tiny_relappmidos is the name of the file!

# we are then able to run the

curl -X 'GET' \
  'http://127.0.0.1:8000/user/users' \
  -H 'accept: text/html' \
  -u "jordi:random_pass"
