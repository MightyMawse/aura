
async function VoteInit(){
    // Add all peers to vote screen
    // Get local user class first
    //var jsonUser = sessionStorage.getItem("user");
    //localUser = JSON.parse(jsonUser);

    var users = await ServerRequest("GET", null, "/get_groupmembers_exclusive?groupID=" + localUser.groupID + "&userID=" + localUser.userID);
    var html = await ServerRequest("GET", null, "/page?name=vote-peer-element", true);
    var parent = document.getElementById("page");
    for(let i = 0; i < users.length; i++){
        var currentUser = users[i]; //id, username, aura, pswrd

        if(currentUser[0] != localUser.userID){
            var peerElement = document.createElement("div");

            peerElement.innerHTML = html;
            peerElement.querySelector("#peer").innerText = currentUser[1];
            peerElement.querySelector("#peer").onclick = function() {CallVote(currentUser[0]);};
            parent.appendChild(peerElement);
        }
    }
}

function ValidAmount(str){
    for(let i = 0; i < str.length; i++){
        var isDigit = (str[i] >= '0' && str[i] <= '9') || str[i] == '-';
        if(!isDigit){
            return false;
        }
    }
    return true;
}

async function CallVote(targetID){
    // Send out vote ping to all peer users
    var voteMade = false;
    while(!voteMade){
        auraAmount = prompt("Aura Amount");
        if(ValidAmount(auraAmount))
            voteMade = true;
    }

    // This will add a vote to the voteMap, every active user will be notified
    var body = {groupID: localUser.groupID, aura: auraAmount, targetID: targetID, senderID: localUser.userID, room: localUser.groupCode};
    //var vote = await ServerRequest("POST", JSON.stringify(body), "/callvote");

    socket.emit("call_vote", JSON.stringify(body)); // Try call the vote
}