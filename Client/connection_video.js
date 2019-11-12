let video               = document.getElementById('video');
let audio               = document.getElementById('audio');
const video_url         = 'http://10.101.20.18:3000/video_url';
// const video_url         = 'http://192.168.43.61:3000';
let supposedCurrentTime = 0;
let request             = new XMLHttpRequest();
let xhttp               = new XMLHttpRequest();
const debug             = true;
const audioBrowser      = false;
const audioHTTP         = true;
let urlTaken            = false;
let intervalUrl, track;


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

/**
 * @return {number}
 */
function EndItemTime(item){
    return item.endTime
}

/**
 * @return {number}
 */
function StartItemTime(item){
    return item.startTime
}

function textItem(item){
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

// Listener for the result of HTTP POST request to Google API
xhttp.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200) {
        let stringAudio = JSON.parse(this.responseText).audioContent;
        console.log("Response arrived");
        audio.src = "data:audio/ogg;base64,"+stringAudio;
        audio.type ="audio/ogg";
        audio.play();

    }else{
        console.log("error");
    }
};

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
            clearInterval(intervalUrl);
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

                    let head = queue.dequeue();
                    let comment_txt = textItem(head);
                    console.log(comment_txt);

                    /**
                     Two different method to call the Google API. First one is to append the API key on http url (The
                     power of API key should be limited). The second one is to append on RequestHeader the authorization
                     through the Bearer token (TO OBTAIN)
                     */

                    if(audioHTTP){
                        xhttp.open("POST", "https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyDgUrhiDmKK0pM8OGpszCoehg2vbRL6pgI", true);
                        xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
                        // xhttp.setRequestHeader("Authorization", "Bearer $(gcloud auth application-default print-access-token)");
                        xhttp.send("{\n" +
                            "    'input':{'text':'"+comment_txt+"'},\n" +
                            "    'voice':{\n" +
                            "      'languageCode':'en-gb',\n" +
                            "      'name':'en-GB-Standard-A',\n" +
                            "      'ssmlGender':'FEMALE'\n" +
                            "    },\n" +
                            "    'audioConfig':{\n" +
                            "      'audioEncoding':'OGG_OPUS'\n" +
                            "    }\n" +
                            "  }");
                    }

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