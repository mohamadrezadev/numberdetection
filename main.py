from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
import model

app = FastAPI()

app.mount("/static", StaticFiles(directory="StaticFiles"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/index")
def index(request:Request,imagename:str=None , data:str=None ):
    return templates.TemplateResponse("index.html", {"request": request,"result":data})



@app.post('/uploadfile')
async def upload_file(request: Request, file: UploadFile = File(...)):
    with open('Upload/uploaded_image.jpg', 'wb') as f:
            f.write(await file.read())
            f.close()
    try:
            
            images= model.getpic('upload/uploaded_image.jpg')
            result=[]
            for i in images:
                    img_border= model.addborder(i)
                    print (img_border)
                    resized_image =model.make_square(img_border)
                    resultmodel= model.testmodel(resized_image)
                    result.append(resultmodel)
            print(result)
            string = ''.join(map(str, result)) 
            print(f.name.lower())
            return templates.TemplateResponse("index.html", {"request": request,"result":string,"image":f'{f.name.lower()}'})
     
             
            # return templates.TemplateResponse("index.html", {"request": 'ds', "title": "My Page", "name": "World","result":result})
    except :
          print("eror")
          return {'status': 'erorr'}


def tem(param):
          return templates.TemplateResponse("index.html", {"request": param, "title": "My Page", "name": "World","result":1})

@app.post('/uploadfileapi/')
async def upload_file(file: UploadFile = File(...)):
    # file_content = await file.read()
        with open('Upload/uploaded_image.jpg', 'wb') as f:
            f.write(await file.read())
            f.close()
    # try:
            
            images= model.getpic('Upload/uploaded_image.jpg')
            result=[]
            for i in images:
                    img_border= model.addborder(i)
                    print (img_border)
                    resized_image =model.make_square(img_border)
                    resultmodel= model.testmodel(resized_image)
                    result.append(resultmodel)
            print(result)    
            return  {"result models":result}
    # except :
    #       print("eror")
    #       return {'status': 'erorr'}
        
   
    # do something with file_content
   
@app.get('/upload/{file}')
async def static_files(file:None or str):
        return FileResponse(f"upload/{file}", media_type="image/png")
        