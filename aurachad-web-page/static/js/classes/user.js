class User{
    static sqlProperty = {
        "USERNAME": 1,
        "AURA": 2,
    };

    groupCode = null;

    constructor(username, userID, aura, groupID){
        this.username = username;
        this.userID = userID;
        this.aura = aura;
        this.groupID = groupID;
    }
}