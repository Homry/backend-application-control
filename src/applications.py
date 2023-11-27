import os
import subprocess
import asyncio
import psutil
from collections import namedtuple
from src.socket import Socket
from src.process_checker import ProcessChecker
from src.database import Database


class Application:
    def __init__(self, socket: Socket, db: Database):
        tmp = os.listdir("/Users")
        default = [
            "All Users",
            "Default",
            "Default User",
            "desktop.ini",
            "Public",
            "Все пользователи",
        ]
        user = [i for i in tmp if i not in default][0]
        self.link = f"/Users/{user}/desktop"
        application = [
            item for item in os.listdir(self.link) if item.split(".")[-1] == "lnk"
        ]
        self.application = {item: f"{self.link}/{item}" for item in application}
        self.app_tuple = namedtuple("app_tuple", "app checker")
        self.open_apps = {}
        self.socket = socket
        self.db = db

    def run_app(self, app_name: str) -> bool:
        if app_name in self.open_apps:
            return False
        application = subprocess.Popen(
            self.application[app_name],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        checker = ProcessChecker(application, app_name, self)
        checker.start()
        if self.db.is_connect():
            self.db.insert_data(app_name, "running")
        self.open_apps[app_name] = self.app_tuple(application, checker)
        return True

    @staticmethod
    def terminate(proc_pid: int) -> None:
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.terminate()
        process.terminate()

    def close_all(self):
        applications = list(self.open_apps.keys())
        for application in applications:
            self.close_app(application)

    def close_app(self, app_name: str) -> bool:
        if app_name in self.open_apps:
            application = self.open_apps[app_name].app
            self.open_apps[app_name].checker.stop()
            self.terminate(application.pid)
            if self.db.is_connect():
                self.db.insert_data(app_name, "stop")
            self.open_apps.pop(app_name)
            return True
        else:
            return False

    def close_manual(self, app_name: str) -> None:
        if self.db.is_connect():
            self.db.insert_data(app_name, "stop")
        self.open_apps.pop(app_name)
        asyncio.run(self.socket.send_message(app_name))

    def get_apps(self) -> list[tuple[str, str]]:
        return list(
            map(
                lambda x: (x, "is running")
                if x in self.open_apps and x in self.application
                else (x, "is not running"),
                self.application,
            )
        )


if __name__ == "__main__":
    app = Application()
    print(app.get_apps())
    app.run_app("Rocket.Chat.lnk")
