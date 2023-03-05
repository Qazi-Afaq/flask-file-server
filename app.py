from flask import Flask  , render_template , request , url_for , redirect
from werkzeug.utils import secure_filename
import os
import math

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

usercontentfolders = os.path.join(os.getcwd() , 'static' , 'usercontentfolders')
# allFolders = os.listdir(usercontentfolders)
allFolders = [f for f in os.listdir(usercontentfolders) if not os.path.isfile(os.path.join(usercontentfolders , f))]
allowedMediaFilesList = ['mp4' , 'png' , 'jpg' , 'jpeg']
allowedImagesFormatsList = ['png' , 'jpg' , 'jpeg']
allowedVideosFormatsList = ['mp4']

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedMediaFilesList


@app.route("/")
def home():
    # allFolders = os.listdir(usercontentfolders)
    allFolders = [f for f in os.listdir(usercontentfolders) if not os.path.isfile(os.path.join(usercontentfolders , f))]
    return render_template('home.html' , allFolders=allFolders , urlForOpeningFolders=url_for('openFolder'))

@app.route('/make-folder' , methods=['POST'])
def makeFolder():
    newFolderName = request.form['new-folder-input'].strip()
    if len(newFolderName.strip()) == 0 or len(newFolderName) > 30:
        print('no empty folder allowed and folder name must be greater than 30 characters')
        return redirect(url_for('home'))
    else:
        try:
            os.mkdir(os.path.join(usercontentfolders , newFolderName))
            if newFolderName not in allFolders:
                allFolders.append(newFolderName)
        except  FileExistsError:
            print("This Folder Already exists")
        except Exception:
            print("An error occured")
    return redirect(url_for('home'))

@app.route("/openspecificfolder/<foldername>")
def openSpecificFolder(foldername):

    try:
        pageNo = abs(int(request.args.get('pg' , 1)))
    except Exception:
        pageNo = 1

    NoOfFilesToShow = 5
    currentFolderMediaPath = os.path.join(os.getcwd() , 'static' , 'usercontentfolders' , foldername)
    start = NoOfFilesToShow * (pageNo-1)
    end = start + NoOfFilesToShow
    totalDirLength = len(os.listdir(currentFolderMediaPath))
    lastPage = math.floor(totalDirLength / NoOfFilesToShow)

    currentFolderMedia = [f for f in os.listdir(currentFolderMediaPath)[start:end] if os.path.isfile(os.path.join(currentFolderMediaPath , f)) and f.split('.')[-1].lower() in allowedMediaFilesList]
    # print(currentFolderMedia)

    kwargsToSend = {
        "folderToOpen":foldername,
        "mediaFilesNames":currentFolderMedia,
        "currentPageNo": pageNo,
        "allowedVideoFormats":allowedVideosFormatsList,
        "allowedImageFormats":allowedImagesFormatsList,
        "totalFilesLength":totalDirLength,
        "NoOfFilesToShow":NoOfFilesToShow,
    }

    return render_template('media.html' , **kwargsToSend , lastPage=lastPage)



@app.route("/open-folder")
def openFolder():
    recievedFolderName = request.args.get('name' , None)
    print(recievedFolderName)
    if not len(recievedFolderName.strip()) == 0 and not recievedFolderName == None and recievedFolderName in allFolders:
        return url_for('openSpecificFolder' , foldername=recievedFolderName)
    else:
        print('Error Cannot open Folder')
        return redirect(url_for('home'))

@app.route("/home_js")
def home_js():
    return render_template("/js/home.js")

@app.route('/upload-files' , methods=['POST'])
def uploadFiles():
    try:
        if (request.form['foldertoopen']):
            folderName = request.form['foldertoopen']      
    except Exception:
        print('cannot get folder name  when uploading file post request')
        return redirect(url_for('home'))

    if 'mediafiles' in request.files:
        for f in request.files.getlist('mediafiles'):
            if not f.filename == '' and f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                if not filename == '':
                    f.save(os.path.join(ROOT_DIR , 'static' , 'usercontentfolders' , folderName , filename))


    return redirect(url_for('openSpecificFolder' , foldername=folderName))