# Fyle Backend (Assignment)

## Setup project with Docker.

```
docker compose up
```

This command will run existing images from docker hub or build new images if they don't exist.

The following containers will start running:

- fyle-interview-intern-backend-core will run on port 7575

```
docker compose build
```

This command will build new images (this will be required when you make changes in Dockerfile or requirements.txt file)



---

## Migrations

In order to run migrations you will have to stop existing running fyle-interview-intern-backend-core container, and run the following commands as per requirement


### Run migrations

```
flask db upgrade -d core/migrations/
```

### How to run shell command
```
docker compose run --rm app sh -c "<command>"
```

---

## Setup project without docker


## Installation

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```
# Code Coverage
Achieved 99% code coverage.
<img width="1470" alt="Screenshot 2024-01-19 at 1 25 23 PM" src="https://github.com/loharvikas/fyle-interview-intern-backend/assets/56187207/7819673f-c14d-4468-80be-7125b4835c0b">

# PyTest
<img width="795" alt="Screenshot 2024-01-19 at 12 59 13 PM" src="https://github.com/loharvikas/fyle-interview-intern-backend/assets/56187207/2a5ea0cc-d2bd-4127-b31c-0e947a62ffa3">

# Added Github actions
<img width="795" alt="Screenshot 2024-01-19 at 12 59 13 PM" src="https://github.com/loharvikas/fyle-interview-intern-backend/assets/56187207/ea8b2c33-07ff-4f8e-8310-c654f851e014">

# Improvements that can be made.
Find the details [Here](https://github.com/loharvikas/fyle-interview-intern-backend/blob/main/Improvement.md)
