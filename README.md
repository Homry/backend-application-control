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
python -m nuitka --standalone --follow-imports  --python-flag=no_site --onefile --remove-output --disable-ccache main.py
```
