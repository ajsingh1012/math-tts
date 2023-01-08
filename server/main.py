from fastapi import FastAPI, UploadFile, File
import pix2tex.api.app as pix2tex

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/upload-tex')
async def upload_tex(file: UploadFile = File(...)):
    '''
    Takes in a `.tex` file, and returns the `.mp3` of the tex
    '''
    return 'upload tex file'


@app.post('/upload-img')
async def upload_image(file: UploadFile = File(...)):
    '''
    Receives an image of a LaTeX equation, and returns the latex
    '''
    # check that the file is an image
    if file.filename and allowed_file(file.filename):
        await pix2tex.load_model()
        latex = await pix2tex.predict(file)
        print(latex)

        return {'latex': latex}

    return {'error': 'file not allowed'}


def allowed_file(filename: str):
    '''
    Checks if a file is "allowed" by seeing its extension
    '''
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS