class Vote:
    groupID = 0
    aura = 0
    targetID = 0
    senderID = 0
    votes = 0
    def __init__(self, groupID, aura, targetID, senderID) -> None:
        self.groupID  = groupID
        self.aura     = aura
        self.targetID = targetID
        self.senderID = senderID