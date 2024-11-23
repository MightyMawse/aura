var localUser = null;
var activeVote = false;
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
    if(localUser.groupID != ""){
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

        // Set group name and code
        var groupCode = await ServerRequest("GET", null, "/group_code?groupID=" + localUser.groupID);
        var group = await ServerRequest("GET", null, "/get_group?groupID=" + localUser.groupID);
        document.getElementById("group").innerText = group[0][1] + ": " + groupCode;
    }
}

async function CheckVote(){
    while(true && localUser.groupID != ""){
        // Check if there is an active vote in voteMap
        await timer(1000);

        // Check if we have a pending vote in our group AND I havent voted yet
        var voteCheck = await ServerRequest("GET", null, "/check_votemap?groupID=" + localUser.groupID + "&userID=" + localUser.userID);

        if(voteCheck != "Ok" && voteCheck != "Error"){ // There are pending votes
            activeVote = true; // Must make a vote
            
            var targetUser = await ServerRequest("GET", null, "/get_user?userID=" + voteCheck.targetID);
            var senderUser = await ServerRequest("GET", null, "/get_user?userID=" + voteCheck.senderID);
            var promptStr = senderUser[0][1] + " Votes to change " + targetUser[0][1] + "'s Aura by: " + voteCheck.aura;

            var prompt = confirm(promptStr); // Vote?

            // Send vote decision
            var voteBody = {userID: localUser.userID, groupID: voteCheck.groupID, vote: prompt};
            var voteRequest = await ServerRequest("POST", JSON.stringify(voteBody), "/submit_vote");
            if(voteRequest == "Error"){
                alert("Internal Error has Occurred, Please Try Again");
            }
        }

        // Also check for change in aura (a disturbance in the force!)
        var updateCheck = await ServerRequest("GET", null, "/check_update?groupID=" + localUser.groupID + "&userID=" + localUser.userID);
        if(updateCheck == "UPDATE"){
            var members = await ServerRequest("GET", null, "/get_groupmembers?groupID=" + localUser.groupID);
            var grid = document.getElementById("peer-grid");

            var elementHTML = await ServerRequest("GET", null, "/page?name=dashboard-peer-element", true);
            var updatedAuraMap = {}; // Get updated aura
            for(const member of members){
                updatedAuraMap[member[1]] = member[2];
            }
            
            // Update aura
            for(const [key, value] of Object.entries(updatedAuraMap)){
                for(const child of grid.children){
                    if(child.querySelector("#username").innerText == key){ // Is this ours to update?
                        child.querySelector("#aura").innerText = value;
                    }
                }
            }
        }
    }
}