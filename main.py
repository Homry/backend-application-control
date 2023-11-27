from multiprocessing import freeze_support

import uvicorn
from src.applications import Application
from src.database import Database
from src.socket import Socket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()
socket = Socket()
db = Database()
application = Application(socket, db)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test</title>
</head>
<body>
<b>127.0.0.1:8000/run/{app_name} - Запустить приложение</b>
<br>
<b>127.0.0.1:8000/stop/{app_name} - Остановить приложение</b>
<br>
<b>127.0.0.1:8000/stop_all - Остановить все приложения</b>
<br>
<b>127.0.0.1:8000/get/app_name - Получить названия всех приложений с их статусами</b>
<br>
<b>127.0.0.1:8000/get/status_all - Получить все записи из бд</b>
<br>
<b>127.0.0.1:8000/get/status/{limit}/{page} - Полуить первые limit записей на page странице</b>
<br>
<b>127.0.0.1:8000/db/{host}/{user}/{password}/{database}/{port} - Подключиться к бд если произошла ошибка подключения </b>
<script>
   let ws = new WebSocket(`ws://localhost:8000/ws`);
    ws.onmessage = function (event) {
        console.log(event.data)
        alert(`${event.data} was closed`)
    };
</script>
</body>
</html>
    """


@app.get("/run/{name}")
async def run(name):
    if application.run_app(name):
        return {"info": f"{name} is running"}
    else:
        return {"info:" f"{name} has already been launched"}


@app.get("/stop/{name}")
async def stop(name):
    if application.close_app(name):
        return {"info": f"{name} is stopped"}
    else:
        return {"info": f"{name} was not started"}


@app.get("/stop_all")
async def stop_all():
    application.close_all()
    return {"info": "close all"}


@app.get("/get/app_name")
async def get_names():
    return {"apps": application.get_apps()}


@app.get("/get/status_all")
async def get_all():
    if db.is_connect():
        return {"db": db.get_data_all()}
    else:
        return {"status": "no connection with db"}


@app.get("/get/status/{limit}/{page}")
async def get_data(limit, page):
    if db.is_connect():
        return {"db": db.get_data_with_pagination(int(limit), int(page))}
    else:
        return {"status": "no connection with db"}


@app.get("/db/{host}/{user}/{password}/{database}/{port}")
async def connect_to_db(host, user, password, database, port):
    if db.connection(host, user, password, database, port):
        return {"status": "connection successful"}
    else:
        return {"status": "no connection with db"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    socket.add_connection(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await websocket.send_text(f"Вы отправили: {data}")
    except WebSocketDisconnect:
        socket.remove_connection(websocket)


if __name__ == "__main__":
    freeze_support()
    uvicorn.run("main:app")
