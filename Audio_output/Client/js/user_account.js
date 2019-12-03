let email           = document.getElementById("email");
let password        = document.getElementById("password");
let firstname       = document.getElementById("firstname");
let lastname        = document.getElementById("lastname");
let r_password      = document.getElementById("password");
let date            = document.getElementById("date");
let r_email         = document.getElementById("email");
let favoriteteam    = document.getElementById("favoriteteam");

function createUser() {

    if((check(r_email) && check(r_password) && check(firstname)
        && check(lastname) && check(date) && check(favoriteteam))) {

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
                    favourite_team: favoriteteam.value
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
    ws.send(JSON.stringify({
        request: "New connection",
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