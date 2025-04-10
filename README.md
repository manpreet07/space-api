# Space-api

- create venv `python3 -m venv venv`
- start venv `source venv/bin/activate`
- install `pip install -r requirements.txt`
- start server `uvicorn app.main:app --reload`

### docker

- build `docker build -t space-api . `
- run `docker run -d -p 4000:80 space-api`
- go to `http://localhost:4000/docs`

### cloud run

- `docker build -t us-central1-docker.pkg.dev/manpreet-singh-07/portfolio/space-api:latest .`
- `docker push us-central1-docker.pkg.dev/manpreet-singh-07/portfolio/space-api:latest`
