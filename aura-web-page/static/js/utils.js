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