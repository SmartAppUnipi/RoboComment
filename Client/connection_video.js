let intervalUrl, track;
let video               = document.getElementById('video');
let audio               = document.getElementById('audio');
let supposedCurrentTime = 0;
let request             = new XMLHttpRequest();
let urlTaken            = false;
const video_url         = 'http://10.101.20.18:3000/video_url';
const debug             = true;
const audioBrowser      = false;
const audioHTTP         = true;


main();


//--------------------------Utils functions-----------------------------------------


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


// HTTP GET request for the video url
function getVideoUrl(req) {
    req.open('GET',video_url);
    req.send();
}


/**
 * @return {number}
 */
function EndItemTime(item){
    return item.json.endTime
}

/**
 * @return {number}
 */
function StartItemTime(item){
    return item.json.startTime
}

function textItem(item){
    return item.json.comment
}

function reqItem(item){
    return item.audio_req
}

function flagItem(item) {
    return item.audio_flag
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


// Say a message Google version
function googleSpeak(item,text){

    let xhttp = reqItem(item);
    setListenerAudio(xhttp,item);

    /**
     Two different method to call the Google API. First one is to append the API key on http url (The
     power of API key should be limited). The second one is to append on RequestHeader the authorization
     through the Bearer token (TO OBTAIN)
     */

    xhttp.open("POST", "https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyDgUrhiDmKK0pM8OGpszCoehg2vbRL6pgI", true);
    xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
    // xhttp.setRequestHeader("Authorization", "Bearer $(gcloud auth application-default print-access-token)");
    xhttp.send("{\n" +
        "    'input':{'text':'"+text+"'},\n" +
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


// Listener addition for the result of HTTP POST request to Google API
function setListenerAudio(xhttp_req, obj){

    xhttp_req.addEventListener("load", function () {
        if (xhttp_req.readyState === 4 && xhttp_req.status === 200) {
            let stringAudio = JSON.parse(xhttp_req.responseText).audioContent;
            obj.audio_flag = 2;
            console.log("Google api response arrived");
            obj.audio_ogg = "data:audio/ogg;base64,"+stringAudio;

        }else{
            console.log("Audio not arrived");
        }
    }, false);
}


// Function to check flag audio to ask for google api and handle listener
function checkFlagAudio(item){

    let flag = flagItem(item);
    let comment_text = textItem(item);
    if(flag === 0){
        console.log("Wait to show comment");

        item.audio_flag = 1;

        if(audioHTTP){
            googleSpeak(item,comment_text);
        }
        if(audioBrowser){
            speak(comment_text, function (e) {
                console.log(e);
            });
        }
    }else if (flag === 1){
        console.log("Wait to show and for synthesized the comment: "+comment_text);
    }else{
        console.log("Wait to show and already get audio: "+comment_text);
    }
}


//----------------------------------------------------------------------------------


//----------------------------Event listener----------------------------------------

// Listener for the result of HTTP request
request.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
        console.log("Response from video server: " + this.responseText);

        urlTaken = true;
        clearInterval(intervalUrl);

        video.src = this.responseText;
        video.type ="video/mp4";
        setTimeout(function () {
            video.play()
        },10000);
    }else{
        console.log("Video unavailable, video server is closed");
        if (debug){
            video.src = "https://storage.googleapis.com/hlt_project/Off_Topic_SA/testvideo.mp4";
            video.type ="video/mp4";
            clearInterval(intervalUrl);
        }
    }
};


// Listener for the CurrentTime event of video
video.addEventListener('timeupdate', (event) => {

    // Seeking disabled in not debug mode
    if(!debug){
        if(!video.seeking){
            supposedCurrentTime = video.currentTime;
        }
    }

    if(!queue.isEmpty()){
        let item = queue.peek();
        if(video.currentTime > EndItemTime(item)){
            if (!video.seeking) {
                console.log("Old comment, remove it from the queue");
                queue.dequeue();
            }
        }else if(video.currentTime < StartItemTime(item)){

            checkFlagAudio(item);

        }else{
            if(track.mode === "showing") {

                let head = queue.dequeue();
                let comment_txt = textItem(head);
                console.log("Show comment: "+comment_txt);

                if(flagItem(head)===2){
                    audio.src = head.audio_ogg;
                    audio.type ="audio/ogg";
                    audio.play();
                }else{
                    console.log("Audio dropped. It did not arrive on time");
                }
                reqItem(head).removeEventListener('load', setListenerAudio, false);
                track.addCue(new VTTCue(video.currentTime, EndItemTime(head), comment_txt));
            }else{
                console.log("Subtitles are disabled from the user");
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

//----------------------------------------------------------------------------------