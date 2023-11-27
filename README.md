# backend-application-control

## Installation
### Create python virualenv
```
python -m venv venv
```

```
venv\Scripts\activate
```

### Install requirements
```
python -m pip install -r requirements.txt
```

### Build .exe
```
python -m nuitka --standalone --follow-imports  --python-flag=no_site --onefile --remove-output --disable-ccache --include-module=main  main.py
```

### Customize .env
Update .env file with your params

For example
```
PG_HOST=127.0.0.1
PG_USER=postgres
PG_PASSWORD=1234
PG_DATABASE=postgres
PG_PORT=5432
```
