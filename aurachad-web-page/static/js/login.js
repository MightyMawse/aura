
async function Login(){
    // Check if login exists
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    var validUsername = username == "" || username == " " ? false : true;
    var validPassword = password == "" || password == " " ? false : true;

    if(!validUsername || !validPassword)
        return;

    username = username.replaceAll(/\s/g,'');
    password = password.replaceAll(/\s/g,'');

    var accountCount = await ServerRequest("GET", null, 
        "/check_account?username="+ username +"&password=" + password);

    if(accountCount[0][0] == 1){
        // Account exists, log in session storage
        LoginProcedure(username, password);
    }
    else if(accountCount[0][0] < 1){
        // Account doesnt exist
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
        alert("Account doesn't exist");
    }
}

async function Register(){
    // Check if login exists
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    var validUsername = username == "" || username == " " ? false : true;
    var validPassword = password == "" || password == " " ? false : true;

    if(!validUsername || !validPassword)
        return;

    username = username.replaceAll(/\s/g,'');
    password = password.replaceAll(/\s/g,'');

    var accountCount = await ServerRequest("GET", null, 
        "/check_account?username="+ username +"&password=" + password);
    
    if(accountCount[0][0] == 0){
        // Account doesnt exist, make it and login
        var body = {username: username, password: password};
        var createAccount = await ServerRequest("POST", JSON.stringify(body), "/create_account");

        // Now login procedure
        LoginProcedure(username, password);
    }
    else{
        // Account already exists, reject
        alert("Account already exists");
    }
}

async function LoginProcedure(username, password){
    // Get full user from db via direct sql query (unsafe?), we need userID
    const query = {query: "SELECT * FROM users WHERE username='"+ username + "' AND password='"+ password +"';"};
    var userData = await ServerRequest("POST", JSON.stringify(query), "/sql_query");

    var user = new User(username, userData[0][0], userData[0][2], ""); // Carry user data over to dashboard

    // Get groupID seperately
    const groupIDQuery = {query: "SELECT groupID FROM partymembers WHERE userID =" + user.userID + ";"};
    var groupID = await ServerRequest("POST", JSON.stringify(groupIDQuery), "/sql_query");
    
    if(groupID.length > 0){
        user.groupID = groupID[0][0]; // Try and set the group id if there is one
    }

    sessionStorage.setItem("user", JSON.stringify(user));
    document.location.href = "/page?name=dashboard"; // Redirect
}