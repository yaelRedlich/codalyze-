from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.services import Analyzer as an
from app.services import Testing_quality_code as tq
import uvicorn
import io
import zipfile

app = FastAPI()

class PathRequest(BaseModel):
    path: str



@app.post("/analyze")
async def create_diagram(request: PathRequest = Body(...)):
    path = request.path
    images = an.create_diagrams(path)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for name, img_buf in images.items():
            img_buf.seek(0)
            zip_file.writestr(f"{name}.png", img_buf.read())

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=diagrams.zip"
    })


@app.post("/alert")
async def warnings(request: PathRequest = Body(...)):
    path = request.path
    return tq.analyze_code(path)


if __name__ == "__main__":
    uvicorn.run("app.routes.API:app", host="127.0.0.1", port=8000, reload=True)
