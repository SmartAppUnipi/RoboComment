let email            = document.getElementById("email");
let password         = document.getElementById("password");
let firstname        = document.getElementById("firstname");
let lastname         = document.getElementById("lastname");
let r_password       = document.getElementById("password");
let date             = document.getElementById("date");
let r_email          = document.getElementById("email");
let favoriteteam     = document.getElementById("favoriteteam");
let favoriteplayer   = document.getElementById("favoriteplayer");
let favoritelanguage = document.getElementById("favoritelanguage");
let favoritevoice    = document.getElementById("favoritevoice");

function createUser() {

    if((check(r_email) && check(r_password) && check(firstname)
        && check(lastname) && check(date) && check(favoriteteam)
        && check(favoritelanguage) && check(favoriteplayer))) {

        showSnack("Send registration");

        ws.send(JSON.stringify({
            request_type: "user_registration",
            request: {
                user: {
                    first_name: firstname.value,
                    last_name: lastname.value,
                    date_of_birth: date.value,
                    email: email.value,
                    password: password.value,
                    favourite_team: favoriteteam.value,
                    favorite_language: favoritelanguage.value,
                    favorite_player: favoriteplayer.value,
                    favorite_voice: favoritevoice.value
                }
            }
        }));
        console.log("Send registration request")
    }
}

function loginUser() {
    if (check(email) && check(password)) {
        ws.send(JSON.stringify({
            request_type: "user_login",
            request: {
                user: {
                    email: email.value,
                    password: password.value
                }
            }
        }));

        console.log("Send login request")
    }
}

function userHello() {
    let location = window.location.href.toString().split("/");
    ws.send(JSON.stringify({
        request: location[location.length - 1],
        request_type: "hello",
        user_id: ifCookie("userId")
    }));
    console.log("Send hello request")
}

function videoListRequest() {
    ws.send(JSON.stringify({
        request_type: "get_videoList",
        request: "",
        user_id: ifCookie("userId")
    }));

    console.log("Send video list request")
}

function sendInfoVideo(matchInfo) {
    ws.send(JSON.stringify({
        request_type: "post_matchID",
        request: matchInfo,
        user_id: ifCookie("userId")
    }));

    console.log("Send hello request")
}

function check(input) {
    if (input.value === null || input.value === "") {
        input.setCustomValidity("Please fill the filed");
        input.reportValidity();

        return false;
    } else {
        // input is fine -- reset the error message
        input.setCustomValidity('');
        input.reportValidity();
        return  true;
    }
}