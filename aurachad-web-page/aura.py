import sql_interface
import vote
import json
import random
from threading import Thread

# Terrible design, refactor later, should be compressed into group class
voteMap = {}
updateMap = {} # groupIDs that need data updated, with an array of userIDs that need to be updated
groupCodeMap = {} # group code to groupID

def Init():
    # Initialise voteMap & groupCodeMap
    query = "SELECT * FROM party;"
    groups = sql_interface.SQLInterface.SQL_query(query)
    for group in groups:
        if(str(group[0]) not in voteMap):
            voteMap.update({str(group[0]): None})

        # Do groupCodeMap
        groupCode = random.randrange(1000, 9999)
        groupCodeMap.update({groupCode: str(group[0])})

def CallVote(groupID, aura, targetID, senderID):
    newVote = vote.Vote(groupID, aura, targetID, senderID)
    if(str(groupID) in voteMap):
        voteMap[str(groupID)] = newVote # Change vote, subsequent votes will overwrite if not resolved
    else:
        voteMap.update({str(groupID): newVote}) # Add it this way if not already in map
    return json.dumps("Ok")

# OBSOLETE
async def CheckVoteMap(groupID, userID):
    try:
        if(voteMap[groupID] != None):
            if(int(userID) in voteMap[groupID].groupMemberIDs):
                return json.dumps(voteMap[groupID].__dict__) # Only send if vote is waiting on sender userID
        return json.dumps("Ok")
    except:
        return json.dumps("Error")

async def SubmitVote(userID, groupID, vote):
    try:
        if(int(userID) in voteMap[str(groupID)].groupMemberIDs): # Member has voted
            voteObj = voteMap[str(groupID)]

            voteObj.Vote(vote) # Submit our vote
            voteObj.groupMemberIDs.remove(int(userID))
            voteMap[str(groupID)].CheckVote() # Check if the vote is complete and can be resolved
        return json.dumps("Ok")
    except:
        return json.dumps("Error")

# OBSOLETE
async def CheckUpdate(groupID, userID):
    if(voteMap[str(groupID)] != None): # Adds to updateFlags
        if(await voteMap[str(groupID)].CheckVote()):
            voteMap[str(groupID)] = None

            # Get members in group
            members = sql_interface.SQLInterface.GetMembers(groupID)
            memberIDs = []
            for member in members:
                memberIDs.append(member[0])
            updateMap.update({groupID: memberIDs}) # Tell everyone that they need to update their ui

    if(groupID in updateMap): # Send update flag only if our group requires update & user has not updated
        if(int(userID) in updateMap[groupID]):
            updateMap[groupID].remove(int(userID))
            return json.dumps("UPDATE")
    return json.dumps("Ok")

async def GetGroupMembersExclusive(groupID, userID):
    query = sql_interface.SQLInterface.queryMap["GET_MEMBERS_EXCLUSIVE"].format(groupID, userID)
    out = sql_interface.SQLInterface.SQL_query(query)
    return json.dumps(out)

async def Join(groupCode, userID):
    try:
        # Add to partymembers db
        # Check if exists first
        groupID = groupCodeMap[int(groupCode)]
        checkQuery = "SELECT COUNT(*) FROM partymembers WHERE groupID = {0} AND userID = {1};"
        checkQuery = checkQuery.format(groupID, userID)
        count = sql_interface.SQLInterface.SQL_query(checkQuery)
        if(count[0][0] == 0):
            query = sql_interface.SQLInterface.queryMap["JOIN_GROUP"].format(groupID, userID)
            sql_interface.SQLInterface.SQL_query(query)
            return json.dumps(groupCodeMap[int(groupCode)]) # Return groupID back to user so he can access their info
        else:
            return json.dumps("Exists")
    except:
        return "Error"
    
# Get group code given the groupID
async def GroupCode(groupID):
    for gc, gID in groupCodeMap.items():
        if(gID == groupID):
            return json.dumps(gc)
    return json.dumps("Error") 