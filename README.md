Mockingbird is a simple testing server which responds back to api requests as configured.


# Installation (local)

## Prerequisites 
   . Mongo
   . Python 3
 
```bash
$ pip install -r requirements.txt
```

```bash
$ python main.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

# Running with Docker (Coming Soon)

# Usage

#### Create a new test endpoint
```bash
$ curl -H "Content-Type: application/json" -XPOST -d '{"project": "testing", "endpoint": "somelist", "methods": ["GET", "POST", "OPTIONS"], "response_body": {"results": [{"id": 1, "name": "XX"}, {"id": 2, "name": "XY"}, {"id": 3, "name": "XZ"}, {"id": 4, "name": "XT"}]}, "response_mime": "application/json"}' http://127.0.0.1:5000/route

{"status_code": 201, "id": "58d1ade37512aa40ce3fed7b"}
```

#### Test new endpoint with  http methods

```bash
$ curl -XGET http://127.0.0.1:5000/api/testing/somelist
{"results": [{"name": "XX", "id": 1}, {"name": "XY", "id": 2}, {"name": "XZ", "id": 3}, {"name": "XT", "id": 4}]}

$ curl -XPOST http://127.0.0.1:5000/api/testing/somelist
{"results": [{"name": "XX", "id": 1}, {"name": "XY", "id": 2}, {"name": "XZ", "id": 3}, {"name": "XT", "id": 4}]}

$ curl -XOPTIONS http://127.0.0.1:5000/api/testing/somelist
{"results": [{"name": "XX", "id": 1}, {"name": "XY", "id": 2}, {"name": "XZ", "id": 3}, {"name": "XT", "id": 4}]}

$ curl -XPUT http://127.0.0.1:5000/api/testing/somelist
{"status_code": 404, "message": "Endpoint not found"}

```
