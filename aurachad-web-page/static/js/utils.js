const timer = ms => new Promise(res => setTimeout(res, ms));

async function ServerRequest(mtd, body, route, rawOverride=false){
    var contentType = rawOverride ? "text/plain" : "application/json";
    const request = await fetch(route, {
        method: mtd,
        headers:{
            "Content-Type": contentType
        },
        body: body
    });
    
    if(rawOverride)
        return await request.text();
    return await request.json();
}

async function LoadOverlay(htmlFile) {
    const html = await ServerRequest("GET", null, "/page?name=" + htmlFile, true);

    var overlay = document.createElement("div");
    overlay.id = "overlay";
    overlay.style = "position: fixed; width: 100%; height: 100%; z-index: 10; top: 0; left: 0; opacity: 1;";
    overlay.innerHTML = html;
    document.body.appendChild(overlay);
    return overlay;
}