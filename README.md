# Flooming-Server

## Installation
before running the server, you need install necessary packages

installing all need packages using this command<br>
```pip install -r requirements.txt```

uvicorn and fastapi are necessary and included in requirements.txt

## Running the server
made by fastapi server can not just run using press the run button on the IDE

open the terminal and type this command <br>
(this command only execute when uvicorn successfully installed) <br>
```uvicorn main:app --reload```

if you occur some error or exception, try this command instead <br>
```python -m uvicorn main:app --reload```

when "Application startup complete is shown", fastapi server is successfully running on port 8000

you can access the server http:/localhost:8000

## Exiting the server
type Ctrl + C in the terminal <br>
then server will shut down