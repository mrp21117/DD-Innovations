const deviceIp = localStorage.getItem("deviceIp");

let eventLogs = []; // Array to store event logs

// Function to fetch and display device status
function fetchDeviceStatus() {
    document.getElementById("device-status-text").innerText = "Online";
    logEvent("Device status: Online"); // Log the device status as "Online"
}

// Function to add a new event log with a timestamp
function logEvent(message) {
    const timestamp = new Date().toLocaleTimeString(); // Get current time
    eventLogs.push(`${timestamp}: ${message}`); // Add new log entry with timestamp

    // Keep only the latest 10 logs
    if (eventLogs.length > 10) {
        eventLogs.shift();
    }

    // Update the log display
    fetchEventLogs();
}

// Function to fetch and display event logs
function fetchEventLogs() {
    const logContainer = document.getElementById("log-container");
    logContainer.innerHTML = ""; // Clear existing logs

    // Display each log entry
    eventLogs.forEach(log => {
        const logItem = document.createElement("p");
        logItem.textContent = log;
        logContainer.appendChild(logItem);
    });
}

// Function to toggle the siren and log the event
function toggleSiren() {
    const sirenButton = document.getElementById("siren-button");
    const toggleUrl = sirenButton.innerText === "Turn Siren On"
        ? `https://${deviceIp}/goform/config?cmd=set&P15470=0`
        : `https://${deviceIp}/goform/config?cmd=set&P15470=1`;

    // Send the siren toggle command
    window.open(toggleUrl, "_blank");
    const newStatus = sirenButton.innerText === "Turn Siren On" ? "Siren started" : "Siren stopped";

    // Log the event
    logEvent(newStatus);

    // Update button text
    sirenButton.innerText = sirenButton.innerText === "Turn Siren On" ? "Turn Siren Off" : "Turn Siren On";
}

// Function to toggle broadcast and log the event
function toggleBroadcast() {
    const broadcastButton = document.getElementById("broadcast-button");
    const accessUrl = `https://${deviceIp}/goform/config?cmd=get&type=sch_open_door`; // Access URL
    const isBroadcastOn = broadcastButton.innerText === "Turn Broadcasting On";
    const toggleUrl = isBroadcastOn
        ? `https://${deviceIp}/goform/config?cmd=set&P15429=1`
        : `https://${deviceIp}/goform/config?cmd=set&P15429=0`;

    // Create a hidden iframe to load the access URL
    const accessIframe = document.createElement("iframe");
    accessIframe.style.display = "none";
    accessIframe.src = accessUrl;
    document.body.appendChild(accessIframe);

    // After access URL loads, toggle the broadcast
    accessIframe.onload = function() {
        // Send the broadcast toggle command
        window.open(toggleUrl, "_blank");
        
        // Log the event
        const newStatus = isBroadcastOn ? "Broadcast started" : "Broadcast stopped";
        logEvent(newStatus);

        // Update button text
        broadcastButton.innerText = isBroadcastOn ? "Turn Broadcasting Off" : "Turn Broadcasting On";

        // Clean up by removing the iframe
        document.body.removeChild(accessIframe);
    };
}

// Function to initialize the live video stream
function initializeVideoStream() {
    const url = `https://admin:admin@${deviceIp}/jpeg/stream`;
    window.open(url, "_blank");
}

// Initialize dashboard elements on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchDeviceStatus();
    initializeVideoStream();
    fetchEventLogs();
});
