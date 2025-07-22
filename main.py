import os.path
import shutil

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from meme_service.base import create_meme

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def base(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def generate(
        request: Request,
        topic: str = Form(...)
):
    if topic:
        # Генерируем картинку
        if os.path.exists(os.path.join("static", "images")):
            shutil.rmtree(os.path.join("static", "images"))
            os.mkdir(os.path.join("static", "images"))
        image_path = create_meme(topic)
        shutil.move(image_path, os.path.join("static", "images", image_path))

        # Возвращаем тот же шаблон, но с путем к картинке
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "image_path": f"images/{image_path}",
                "topic": topic
            }
        )
    else:
        return templates.TemplateResponse("index.html", {"request": request})
