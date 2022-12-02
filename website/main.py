from flask import Flask, render_template, request, send_file, flash
from pytube import YouTube
from glob import glob
import os

app = Flask(__name__)
app.secret_key = 'super secret'

    
    


@app.route("/")
def homePage():
    # Check downloads dir is empty and delete contents if not.
    if os.listdir('downloads'):
        files = glob("./downloads/*")[0]
        if files:
            os.remove(files)
    
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def downloadPage():

    #use user provided YouTube url to download video from YouTube into downloads folder
    if request.method == "POST":
        if not request.form['link']:
            flash("Enter a valid url")
            return render_template("download.html", msg=1)
        else:
            try:    
                #fetching video from Youtube
                link = request.form["link"] 
                youtube = YouTube(link)
                youtubeObject = youtube.streams.get_highest_resolution()
                title = youtube.title
                global img
                img = youtube.thumbnail_url
                youtubeObject.download('downloads')

                flash("Video ready to download, click download button")
                return render_template("download.html",title=title, image=img, msg=2, link=link)

            except:
                flash("Error: Video could not be downloaded")
                return render_template("download.html", msg=1)
            
    else:
        return render_template("index.html")

@app.route('/sucess')
def sucessPage():
    # return message to user
    flash("Download is complete")
    return render_template('download.html', msg=3,image=img, enablejs=True )

@app.route('/file')
def serveFile():
    # serve downloaded video to user
    filename = glob("./downloads/*.mp4")[0]

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
