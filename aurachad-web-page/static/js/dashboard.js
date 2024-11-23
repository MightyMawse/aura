var localUser = null;
var activeVote = false;
var socket = null;

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
        localUser.groupCode = groupCode;
    }

    SocketInit()
}

function SocketInit(){
    socket = io();
        socket.on('connect', function() {
            console.log('Connected to server');
        });
        socket.on('message', function(msg) { 
            SocketMessageHandler(msg)
        });
        socket.on('disconnect', function() {
            console.log('Disconnected from server');
        });
        
        if(localUser.groupCode != null){
            var data = {"username": localUser.username, "room": localUser.groupCode};
            socket.emit("join", data); // try join
        }
}

// Handles the socket messages
async function SocketMessageHandler(msg){
    console.log(msg);
    var jsonObj = JSON.parse(msg);

    // Vote prompt
    if(jsonObj.type == "VOTECALL"){

        var sender = await ServerRequest("GET", null, "/get_user?userID=" + jsonObj.content.senderID);
        var target = await ServerRequest("GET", null, "/get_user?userID=" + jsonObj.content.targetID);

        var promptString = sender[0][1] + " votes to change " + target[0][1] + "'s aura by " + jsonObj.content.aura;
        var decision = confirm(promptString);

        // Submit the vote
        var submitBody = {userID: localUser.userID, groupID: localUser.groupID, vote: decision};
        await ServerRequest("POST", JSON.stringify(submitBody), "/submit_vote");
    }
}

async function Join(){
    localUser = JSON.parse(sessionStorage.getItem("user"));

    var groupCode = document.getElementById("gc").value;
    var groupID = await ServerRequest("GET", null, "/join?groupCode=" + groupCode + "&userID=" + localUser.userID);
    
    if(groupID != "Error"){
        localUser.groupID = groupID;
        sessionStorage.setItem("user", JSON.stringify(localUser));

        // Tell others to refresh their dashboard

        // Reset overlay
        document.getElementById("overlay").remove();
        overlay = null;

        Init(); // Re-initialize dashboard
    }
    else if(groupID == "Exists"){
        alert("Already in Group");
    }
    else{
        alert("Group Doesn't Exist");
    }
}