from pathlib import Path
from fastapi import APIRouter
from loguru import logger as loguru_logger
from app.core.logging import get_logger
from app.schemas.client_log import ClientLogIn

router = APIRouter(prefix="/logs", tags=["logs"])
app_logger = get_logger()

Path("logs").mkdir(exist_ok=True)
loguru_logger.add(
    "logs/client.log",
    rotation="5 MB",
    level="INFO",
    filter=lambda record: record["extra"].get("source") == "client",
)


@router.post("/client", status_code=201)
def receive_client_log(payload: ClientLogIn):
    text = (
        f"[CLIENT][{payload.level.upper()}] {payload.message} | "
        f"url={payload.url} | time={payload.timestamp} | context={payload.context}"
    )
    if payload.stack:
        text += f" | stack={payload.stack}"

    client_file_logger = loguru_logger.bind(source="client")

    if payload.level == "error":
        app_logger.error(text)
        client_file_logger.error(text)
    elif payload.level == "warn":
        app_logger.warning(text)
        client_file_logger.warning(text)
    else:
        app_logger.info(text)
        client_file_logger.info(text)

    return {"status": "ok"}
