// Authentication page functions
function getDeviceIp() {
    return document.getElementById("device-ip").value;
}

function saveDeviceIp() {
    const deviceIp = document.getElementById("device-ip").value;
    if (deviceIp) {
        localStorage.setItem("deviceIp", deviceIp);
    } else {
        alert("Please enter the Device IP.");
    }
}

function getChallengeCode() {
    saveDeviceIp();  // Store the device IP for later use

    const deviceIp = localStorage.getItem("deviceIp");  // Retrieve from localStorage
    if (!deviceIp) {
        alert("Please enter the Device IP.");
        return;
    }

    const url = `https://${deviceIp}/goform/login?cmd=login&user=admin&type=0`;
    window.open(url, "_blank");
}


function generateAuthCode(event) {
    event.preventDefault();
    const challengeCode = document.getElementById("challenge-input").value;
    if (!challengeCode) {
        alert("Please enter a valid Challenge Code");
        return;
    }
    const combinedText = `${challengeCode}:GDS3710lZpRsFzCbM:admin`;
    const authCode = CryptoJS.MD5(combinedText).toString(CryptoJS.enc.Hex);
    document.getElementById("auth-code").innerText = authCode;
    document.getElementById("auth-input").value = authCode;
}

function openDashboard(event) {
    event.preventDefault();
    const deviceIp = getDeviceIp();
    const authCode = document.getElementById("auth-input").value;

    if (!deviceIp) {
        alert("Please enter the Device IP.");
        return;
    }
    if (!authCode) {
        alert("Please enter a valid Authentication Code");
        return;
    }

    // Construct the login URL with the authentication code
    const loginUrl = `https://${deviceIp}/goform/login?cmd=login&user=admin&authcode=${authCode}&type=0`;

    // Open the access URL in the same window to authenticate
    window.open(loginUrl, "_blank");

    // After login, load the dashboard in the same window
    // You can add a redirect to dashboard.html after the login URL completes
    // Assuming loginUrl redirects or you manually handle the login redirect:
    setTimeout(() => {
        window.location.href = "dashboard.html"; // Load dashboard page after successful login
    }, 2000); // Adjust the delay time based on how long login takes to process
}


// Attach event listeners for form submission
document.getElementById("password-form").addEventListener("submit", generateAuthCode);
document.getElementById("login-form").addEventListener("submit", openDashboard);
