import sql_interface
import main

class Vote:
    groupID = 0
    aura = 0
    targetID = 0
    senderID = 0
    groupMemberIDs = []
    def __init__(self, groupID, aura, targetID, senderID) -> None:
        self.groupID  = groupID
        self.aura     = aura
        self.targetID = targetID
        self.senderID = senderID

        # Initialise groupMemberIDs, this is so we can keep track of who has voted
        members = sql_interface.SQLInterface.GetMembers(groupID)
        for member in members:
            self.groupMemberIDs.append(member[0])

    # Check if vote has been resolved
    def CheckVote(self):
        if(len(self.groupMemberIDs) == 0):
            # Update aura
            currentAura = sql_interface.SQLInterface.GetAura(self.targetID)
            alteredAura = currentAura[0][0] + int(self.aura)
            query = "UPDATE users SET aura = {0} WHERE userID = {1};".format(alteredAura, self.targetID)
            sql_interface.SQLInterface.SQL_query(query)
            #main.voteMap[str(self.groupID)] = None # NOT WORKING, FIND WAY TO REMOVE CLASS FROM MAP!
            return True
        return False
