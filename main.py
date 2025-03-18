import os
import logging

from fastapi import FastAPI, Response, status
import psycopg2
from redis import StrictRedis

app = FastAPI()
redis = StrictRedis.from_url(os.environ["REDIS_URL"])
logger = logging.getLogger('uvicorn.error')

def get_db():
    """Instantiate a connection to the Database."""
    return psycopg2.connect(os.environ["DATABASE_URL"])


@app.get("/health")
def simple_health_check():
    return {"message": "healthy"}


@app.get("/health-full")
def complete_health_check(response: Response):
    try:
        redis.ping()
    except Exception as err:
        logger.error('could not ping Redis %s', err)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "message": "complete health check failed", 
            "reason": "redis unreachable",
        }

    try:
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute("SELECT 1;")
                logger.debug(curs.fetchone())
    except Exception as err:
        logger.error('could not access postgresql %s', err)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "message": "complete health check failed", 
            "reason": "postgres unreachable",
        }
    return {"message": "complete health check is healthy"}


@app.get("/")
def read_root():
    return {"Hello": "World"}
