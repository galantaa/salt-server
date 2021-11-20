# Salt Server
validate requests -- lightning fast 💨

## API
There are 2 endpoints:
  - post "/model/"
  send a valid model to upload to DB
  - post "/requests/validate"
  send a request to validate it

## Run locally
clone the repo,
create a python venv and activate it
```
$ python3 -m venv venv
$ source venv/bin/activate
```
install packages
```
$ pip3 install fastapi
$ pip3 install "uvicorn[standard]"
```
run
```$ python3 main.py```

Now you can send your requests :)

## Run tests
```$ python3 -m unittest -v```

## Discussion
  - I Used FastAPI because it is considered fast for handling requests,
   fast to code, and it is well adopted.
  Also, I wanted to get to know it.
  - I saved the models in-memory,
   but if I had more time I'd use a NoSql DB,
   which can support the document structure I used to save the models,
   and it is also considered the right solution for high traffic,
   as this server needs to handle.

    I'd use MongoDB because it should be great in terms of performance,
   and it is well adopted and considered robust and easy to install and maintain.

  - If I'd used a DB, the web server should support async I/O well.
   I know that Tornado is good for that.
