var localUser = null;
async function Init(){
    var jsonUser = sessionStorage.getItem("user");
    var user = JSON.parse(jsonUser);
    localUser = user;

    // Set user welcome msg
    document.getElementById("username").innerText = "Welcome " + localUser.username;

    // Set aura count
    var aura = await ServerRequest("GET", null, "/get_aura?userID=" + localUser.userID);
    document.getElementById("aura_count").innerText = aura[0][0];

    // Load peers
    // Check if userID exists in partymember db
    // If it does, get all users in group
    var members = await ServerRequest("GET", null, "/get_groupmembers?groupID=" + localUser.groupID);
    var elementHTML = await ServerRequest("GET", null, "/page?name=dashboard-peer-element", true);
    var grid = document.getElementById("peer-grid");
    for(let i = 0; i < members[0].length; i++){
        var newElement = document.createElement("div");
        newElement.innerHTML = elementHTML;

        // Set new element info
        newElement.querySelector("#username").innerText = members[i][1];
        newElement.querySelector("#aura").innerText = members[i][2];
        grid.appendChild(newElement);
    }
}

async function CheckVote(){
    while(true){
        // Check if there is an active vote in voteMap
        await timer(1000);

        var voteCheck = await ServerRequest("GET", null, "/check_votemap?groupID=" + localUser.groupID);

        if(voteCheck.length > 0){ // There are pending votes
            for(let i = 0; i < voteCheck.length; i++){ // Foreach vote
                var jsonObj = JSON.parse(voteCheck[i]);
                var targetUser = await ServerRequest("GET", null, "/get_user?userID=" + jsonObj.targetID);
                var senderUser = await ServerRequest("GET", null, "/get_user?userID=" + jsonObj.senderID);
                var promptStr = senderUser[0][1] + " votes to change " + targetUser[0][1] + "'s aura by " + jsonObj.aura;
                var prompt = confirm(promptStr);
            }
        }
    }
}