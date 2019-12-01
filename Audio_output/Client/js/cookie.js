function setCookie(cname, cvalue, hours) {
    let d = new Date();
    d.setTime(d.getTime() + (hours*60*60*1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    let user=getCookie("username");
    if (user !== "") {
        alert("Welcome again " + user);
    } else {
        user = prompt("Please enter your name:","");
        if (user !== "" && user != null) {
            setCookie("username", user, 30);
        }
    }
}

function ifCookie(field) {
    let cookie = getCookie(field);
    if (cookie === "")
        return 0;
    else
        return cookie;
}