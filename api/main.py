from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import DESCENDING

from config import get_db

print(">>> ŁADUJĘ TEN PLIK MAIN.PY <<<")

app = FastAPI(title="Log System Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = get_db()
logs_col = db["logs"]


def serialize_log(doc):
    return {
        "id": str(doc.get("_id")),
        "timestamp": doc.get("timestamp"),
        "service": doc.get("service"),
        "level": doc.get("level"),
        "message": doc.get("message"),
        "host": doc.get("host"),
        "environment": doc.get("environment"),
    }


# ---------------- ERRORS BY SERVICE ----------------

@app.get("/stats/errors-by-service")
def errors_by_service(environment: Optional[str] = Query(None)):

    match_stage = {"level": "ERROR"}

    if environment:
        match_stage["environment"] = environment

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": "$service",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    return list(logs_col.aggregate(pipeline))


# ---------------- ERRORS TREND ----------------

@app.get("/stats/errors-trend")
def errors_trend():

    pipeline = [
        {"$match": {"level": "ERROR"}},

        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"},
                    "hour": {"$hour": "$timestamp"},
                    "minute10": {
                        "$subtract": [
                            {"$minute": "$timestamp"},
                            {
                                "$mod": [
                                    {"$minute": "$timestamp"},
                                    10
                                ]
                            }
                        ]
                    }
                },
                "count": {"$sum": 1}
            }
        },

        {
            "$sort": {
                "_id.year": 1,
                "_id.month": 1,
                "_id.day": 1,
                "_id.hour": 1,
                "_id.minute10": 1
            }
        }
    ]

    data = list(logs_col.aggregate(pipeline))

    return [
        {
            "date": (
                f"{d['_id']['year']}-"
                f"{d['_id']['month']:02d}-"
                f"{d['_id']['day']:02d} "
                f"{d['_id']['hour']:02d}:"
                f"{d['_id']['minute10']:02d}"
            ),
            "count": d["count"]
        }
        for d in data
    ]


# ---------------- LOGS ----------------

@app.get("/logs/latest")
def latest_logs(
    limit: int = Query(100, ge=1, le=1000),
    level: Optional[str] = Query(None),
    service: Optional[str] = Query(None),
    environment: Optional[str] = Query(None),
):
    query = {}

    if level:
        query["level"] = level

    if service:
        query["service"] = service

    if environment:
        query["environment"] = environment

    cursor = (
        logs_col.find(query)
        .sort("timestamp", DESCENDING)
        .limit(limit)
    )

    return [serialize_log(doc) for doc in cursor]


# ---------------- LIVE STREAM ----------------

@app.websocket("/ws/logs")
async def websocket_logs(ws: WebSocket):

    await ws.accept()

    try:
        with logs_col.watch(
            [{"$match": {"operationType": "insert"}}]
        ) as stream:

            for change in stream:

                doc = change.get("fullDocument")

                if not doc:
                    continue

                await ws.send_json(
                    serialize_log(doc)
                )

    except WebSocketDisconnect:
        return

    except Exception as e:
        print("WebSocket error:", e)
        await ws.close()

@app.get("/debug/watch")
def debug_watch():
    try:
        with logs_col.watch() as stream:
            return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}