from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()

# Templates folder to store HTML templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def mainpage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 'result': "NA"})



@app.post("/submit")
def input(request: Request, text_input: str = Form(...)):
    if text_input == "":
        text_input = "NA"
    print("User input: ", text_input)
    with open('dump.txt', 'a') as file:
        file.write(text_input + '\n')
    return templates.TemplateResponse('index.html', context={'request': request, 'result': text_input})
