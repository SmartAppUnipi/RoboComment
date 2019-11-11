let video               = document.getElementById('video');
const video_url      = 'http://192.168.43.61:3000/video_url';
// const video_url         = 'http://192.168.43.61:3000';
let supposedCurrentTime = 0;
let request             = new XMLHttpRequest();
const debug             = false;
const audioBrowser      = true;
const audioHTTP         = false;
let urlTaken            = false;
let intervalUrl, track;
// const GOOGLE_APPLICATION_CREDENTIALS = "My First Project-783591cd0d97.json";


main();


//---------------------Utils functions---------------------------------

function main() {

    // Add track for dynamic subtitles
    track = video.addTextTrack("captions", "English", "en");
    track.mode = "showing";

    intervalUrl = setInterval(function () {
        if(!urlTaken) {
            getVideoUrl(request);
        }
    },1000);
}

// HTTP GET request
function getVideoUrl(req) {
    req.open('GET',video_url);
    req.send();
}

function EndItemTime(item){
    // let obj = JSON.parse(item);
    return item.end
}

function StartItemTime(item){
    // let obj = JSON.parse(item);
    return item.start
}

function textItem(item){
    // let obj = JSON.parse(item);
    return item.comment
}

// Say a message
function speak(text, callback) {
    let u = new SpeechSynthesisUtterance();
    u.text = text;
    u.lang = 'en-US';

    u.onend = function () {
        if (callback) {
            console.log("in END");
            callback();
        }
    };

    u.onerror = function (e) {
        if (callback) {
            console.log("in ERROR");
            callback(e);
        }
    };

    speechSynthesis.speak(u);
}

//---------------------------------------------------------------------


//------------------------Event listener-------------------------------

// Listener for the result of HTTP request
request.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
        console.log("Response: " + this.responseText);

        urlTaken = true;
        clearInterval(intervalUrl);

        video.src = this.responseText;
        video.type ="video/mp4";
        setTimeout(function () {
            video.play()
        },10000);
    }else{
        console.log("Video unavailable");
        if (debug){
            video.src = "https://storage.googleapis.com/hlt_project/Off_Topic_SA/testvideo.mp4";
            video.type ="video/mp4";
        }
    }
};


// Listener for the CurrentTime event of video
video.addEventListener('timeupdate', (event) => {

    if(!debug){
        if(!video.seeking){
            supposedCurrentTime = video.currentTime;
        }
    }

    if(track!=null){
        if(!queue.isEmpty()){
            let item = queue.peek();
            if(video.currentTime > EndItemTime(item)){
                if (!video.seeking) {
                    console.log("remove");
                    queue.dequeue();
                }
            }else if(video.currentTime < StartItemTime(item)){
                console.log("wait to show");
            }else{
                console.log("show");

                if(track.mode === "showing") {

                    if(audioHTTP){
                        xhttp.open("POST", "https://texttospeech.googleapis.com/v1/text:synthesize", true);
                        xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
                        xhttp.setRequestHeader("Authorization", "Bearer $(gcloud auth application-default print-access-token)");
                        xhttp.send("{\n" +
                            "    'input':{\n" +
                            "      'text':'Android is a mobile operating system developed by Google,\n" +
                            "         based on the Linux kernel and designed primarily for\n" +
                            "         touchscreen mobile devices such as smartphones and tablets.'\n" +
                            "    },\n" +
                            "    'voice':{\n" +
                            "      'languageCode':'en-gb',\n" +
                            "      'name':'en-GB-Standard-A',\n" +
                            "      'ssmlGender':'FEMALE'\n" +
                            "    },\n" +
                            "    'audioConfig':{\n" +
                            "      'audioEncoding':'MP3'\n" +
                            "    }\n" +
                            "  }");
                    }

                    let head = queue.dequeue();
                    console.log(EndItemTime(head));
                    let comment_txt = textItem(head);

                    if(audioBrowser){
                        speak(comment_txt, function (e) {
                            console.log(e);
                        });
                    }

                    track.addCue(new VTTCue(video.currentTime, EndItemTime(head), comment_txt));
                }
            }
        }
    }
});

//Listening for seeking. Id debug is true than seeking is deactivated
video.onseeking = function() {
    if (!debug){
        let delta = video.currentTime - supposedCurrentTime;
        if(Math.abs(delta)>0.01){
            console.log("Seeking no");
            video.currentTime = supposedCurrentTime;
        }
    }
};

// Listener for the ending of the video
video.addEventListener('ended', function () {
   if (!debug){
       supposedCurrentTime = 0;
   }
});

//---------------------------------------------------------------------