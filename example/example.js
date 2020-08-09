function getAllData(){
	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    	let url = tabs[0].url;
    	// use `url` here inside the callback because it's asynchronous!
	});
}

/*
"permissions": [ ...
   "tabs"
]
*/

//in content.js
chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.text === 'report_back') {
        const result = ["cotton","polyester","hemp","organic cotton","wool","nylon"].filter(m=>document.documentElement.innerText.indexOf(m)>-1)
        sendResponse(result);
    }
});