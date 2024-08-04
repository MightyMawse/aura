
async function ServerRequest(mtd, body, route){
    const request = await fetch(route, {
        method: mtd,
        headers:{
            "Content-Type": "application/json"
        },
        body: body
    });
    
    return await request.json();
}