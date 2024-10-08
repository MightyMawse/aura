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
    for(let i = 0; i < members.length; i++){
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

        // Check if we have a pending vote in our group AND I havent voted yet
        var voteCheck = await ServerRequest("GET", null, "/check_votemap?groupID=" + localUser.groupID + "&userID=" + localUser.userID);

        if(voteCheck != "Ok"){ // There are pending votes
            var targetUser = await ServerRequest("GET", null, "/get_user?userID=" + voteCheck.targetID);
            var senderUser = await ServerRequest("GET", null, "/get_user?userID=" + voteCheck.senderID);
            var promptStr = senderUser[0][1] + " Votes to change " + targetUser[0][1] + "'s Aura by: " + voteCheck.aura;

            var prompt = confirm(promptStr); // Vote?
            if(prompt){
                // Send vote decision
                var voteBody = {userID: localUser.userID, groupID: voteCheck.groupID, vote: prompt};
                await ServerRequest("POST", JSON.stringify(voteBody), "/submit_vote");
            }
        }

        // Also check for change in aura (a disturbance in the force!)
        var updateCheck = await ServerRequest("GET", null, "/check_update?groupID=" + localUser.groupID);
        if(updateCheck == "UPDATE"){
            var members = await ServerRequest("GET", null, "/get_groupmembers?groupID=" + localUser.groupID);
            var grid = document.getElementById("peer-grid");

            grid.children.array.forEach(element => {
                element.remove(); // Clear current and rebuild
            });

            for(let i = 0; i < members.length; i++){
                var elementHTML = await ServerRequest("GET", null, "/page?name=dashboard-peer-element", true);
                var newElement = document.createElement("div");
                newElement.innerHTML = elementHTML;

                // Set new element info
                newElement.querySelector("#username").innerText = members[i][1];
                newElement.querySelector("#aura").innerText = members[i][2];
                grid.appendChild(newElement);
            }
        }
    }
}