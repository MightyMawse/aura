var localUser = null;

async function Init(){
    // Add all peers to vote screen
    // Get local user class first
    var jsonUser = sessionStorage.getItem("user");
    localUser = JSON.parse(jsonUser);

    var users = await ServerRequest("GET", null, "/get_groupmembers?groupID=" + localUser.groupID);
    var html = await ServerRequest("GET", null, "/page?name=vote-peer-element", true);
    var parent = document.getElementById("page");
    for(let i = 0; i < users.length; i++){
        var currentUser = users[i]; //id, username, aura, pswrd
        var peerElement = document.createElement("div");

        peerElement.innerHTML = html;
        peerElement.querySelector("#peer").innerText = currentUser[1];
        //var click = "CallVote(" + currentUser[0] + ")";
        peerElement.querySelector("#peer").onclick = function() {CallVote(currentUser[0]);};
        parent.appendChild(peerElement);
    }
}

async function CallVote(targetID){
    // Send out vote ping to all peer users
    var auraAmount = prompt("Aura amount");

    // This will add a vote to the voteMap, every active user will be notified
    var body = {groupID: localUser.groupID, aura: auraAmount, targetID: targetID, senderID: localUser.userID};
    var vote = await ServerRequest("POST", JSON.stringify(body), "/callvote");
}