// Define API URLs as variables
const apiUrls = {
    systemActivate: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=SYSACT%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    systemDeactivate: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=SYSDEACT%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    panicOn: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=PANICON%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    panicOff: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=PANICOFF%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    sirenOn: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=SIREN,ON%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    sirenOff: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=SIREN,OFF%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    extendedHooterOn: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=WL_SIREN,ON%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
    extendedHooterOff: 'https://portal.vasudevsms.in/api/mt/SendSMS?user=DDInnovation0622&password=PC480riEL6JY&senderid=DDINNS&channel=Trans&DCS=0&flashsms=0&number=916359285046&text=WL_SIREN,OFF%0Aby%20DDInnovations&route=2&DLTSenderId=1301165354970713260',
  };  

  // Function to trigger an API call
  function triggerAPI(url, actionName) {
    const iframe = document.getElementById('hiddenFrame');
    iframe.src = url; // Set the iframe's src to the API URL
  
    // Log a message to the report dashboard
    addReportMessage(`Triggered ${actionName} at ${new Date().toLocaleTimeString()}`);
  }
  
  // Function to add a message to the Report Dashboard
  function addReportMessage(message) {
    const reportList = document.getElementById('reportList');
    const listItem = document.createElement('li');
    listItem.textContent = message; // Set the message text
    reportList.appendChild(listItem); // Add the message to the list
  }
  