# REST API application

Simple REST API application for getting food nutrition value. 

## REST API

### Get nutrition value 

```
GET /nutrition/{food_name}
```

### Add new nutrition information

```
POST /nutrition
```

## Usage

Run the server locally and access it at `localhost:8000`:

```
uvicorn app.main:app --reload
```

Or run the server in a Docker container and access it at `localhost`:
```
docker run -d -p 80:80 myimage
```