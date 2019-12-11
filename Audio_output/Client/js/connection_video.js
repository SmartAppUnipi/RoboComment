let track, videoUrl, videoId, videoType;
let video               = document.getElementById('video');
let audio               = document.getElementById('audio');
let supposedCurrentTime = 0;
let request             = new XMLHttpRequest();
const debug             = false;
const audioBrowser      = false;
const audioHTTP         = true;


main();


//--------------------------Utils functions-----------------------------------------


function main() {

    // Add track for dynamic subtitles
    track = video.addTextTrack("captions", "MultiLingual", "en");
    // track.scroll = "none";
    track.mode = "showing";

    videoUrl = getCookie("videoURL");
    videoId = getCookie("videoID");
    videoType = getCookie("videoType");

    console.log("User_ID: "+ ifCookie("userId"));
    console.log("Video ID: " + videoId);

    if(videoUrl!==''){
        video.src = videoUrl;
        video.type = "video/mp4";
        setTimeout(function () {
            playVideo()
        }, 10000);
    } else{
        window.location.href = "catalog.html";

    }
}

function playVideo() {
    video.play();
    if (videoType !== '' && videoType === "realtime") {
        console.log(video.currentTime);
        video.currentTime = 20;
        console.log(video.currentTime);
        console.log("Start realtime");
    }
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

function emphasyItem(item) {
    return item.json.emphasis
}

function languageItem(item){
    if(!item.json.language){
        return "en";
    }else{
        return item.json.language;
    }
}

function voiceItem(item){

    if(!item.json.voice){
        if(languageItem(item)==="en"){
            return "en-US-Wavenet-D";
        }else{
            return  "it-IT-Wavenet-D";
        }
    }else{
        return item.json.voice;
    }
}

function calcolateRate(emphasy){
    switch (emphasy) {
        case 1: { return "medium"}
        // case 2: { return 100}
        case 3: { return "default"}
        // case 4: { return 5}
        case 5: { return "medium"}
    }
}

function calcolatePitch(emphasy){
    switch (emphasy) {
        case 1: { return "high"}
        // case 2: { return 10}
        case 3: { return "default"}
        // case 4: { return 5}
        case 5: { return "x-low"}
    }
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
    let nameVoice = voiceItem(item);
    let lanCode;
    if(languageItem(item) === "it"){
        lanCode   = 'it-IT';
    }else{
        lanCode   = 'en-US';
    }

    xhttp.open("POST", "https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyDgUrhiDmKK0pM8OGpszCoehg2vbRL6pgI", true);
    xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");

    let rate    = calcolateRate(emphasyItem(item));
    let pitch   = calcolatePitch(emphasyItem(item));

    console.log("Asking for audio with voice: " + nameVoice + " and language:" + lanCode);
    xhttp.send(JSON.stringify({
        input: {ssml: "<speak><prosody rate=\"" + rate + "\" pitch=\"" + pitch + "\" >" + text + "</prosody></speak>" },

        voice: {
            languageCode: lanCode,
            name: nameVoice
        },
        audioConfig: {
            audioEncoding: 'OGG_OPUS'
        }
    }));
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


// Listener for the ending of the video
video.addEventListener('ended', function () {
   if (!debug){
       supposedCurrentTime = 0;
   }
});

//----------------------------------------------------------------------------------