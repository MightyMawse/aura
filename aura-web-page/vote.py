import sql_interface
import main

class Vote:
    groupID = 0
    aura = 0
    targetID = 0
    senderID = 0
    memberCount = 0
    groupMemberIDs = []
    resolved = False
    yesVotes = 0
    noVotes = 0
    alteredAura = 0

    def __init__(self, groupID, aura, targetID, senderID) -> None:
        self.groupID  = groupID
        self.aura     = aura
        self.targetID = targetID
        self.senderID = senderID

        # Initialise groupMemberIDs, this is so we can keep track of who has voted
        members = sql_interface.SQLInterface.GetMembers(groupID)
        for member in members:
            self.groupMemberIDs.append(member[0])
            self.memberCount += 1

        currentAura = sql_interface.SQLInterface.GetAura(self.targetID)
        self.alteredAura = currentAura[0][0] + int(self.aura)

    # Submit vote
    def Vote(self, vote):
        if(vote):
            self.yesVotes += 1
        else:
            self.noVotes += 1

    # Check if vote has been resolved
    async def CheckVote(self):
        allVotesMade = True if self.yesVotes + self.noVotes == self.memberCount else False
        if(len(self.groupMemberIDs) == 0 & self.resolved == False & allVotesMade):
            # Update aura
            self.resolved = True

            if(self.yesVotes > self.noVotes):
                query = "UPDATE users SET aura = {0} WHERE userID = {1};".format(self.alteredAura, self.targetID)
                sql_interface.SQLInterface.SQL_query(query)
                
            return True
        return False
