import sql_interface

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