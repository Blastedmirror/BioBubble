# PlayerNode class
class PlayerNode:
    def __init__(self, Pid):
        self.Pld = Pid
        self.attrCtr = 1
        self.left = None
        self.right = None


# Insertion method
def insert(pNode, Pid):
    node = search(pNode, Pid)
    if node is None:
        # means theres no such player in the tree hence add new player node.
        if pNode is None:
            return PlayerNode(Pid)
        else:
            if pNode.Pld == Pid:
                return pNode
            elif pNode.Pld < Pid:
                pNode.right = insert(pNode.right, Pid)
            else:
                pNode.left = insert(pNode.left, Pid)
    else:
        # means the tree has player with the same ID and that players swipe count increases.
        node.attrCtr += 1
    return pNode


# Searches the tree to find any player with same ID.
# If theres no such player returns nothing.
def search(pNode, Pid):
    if pNode is None:
        return None
    if pNode.Pld == Pid:
        return pNode
    if pNode.Pld < Pid:
        return search(pNode.right, Pid)
    return search(pNode.left, Pid)


# This is a method to transverse through the tree
def inorder(pNode):
    if pNode:
        inorder(pNode.left)
        print("Player ID =", pNode.Pld, "Swipe count= ", pNode.attrCtr)
        inorder(pNode.right)


# operation 1
# This method reads from the input file and creates the tree of players with their swipe count.
# returns the root node of created tree
def _recordSwipeRes():
    file = open("inputPS12.txt", "r")
    l = file.readlines()
    bst = PlayerNode(int(l[0]))
    for i in range(1, len(l)):
        bst = insert(bst, int(l[i]))
    file.close()
    return bst


# operation 2
# This method counts the total number of players who came to hotel today.
def _getSwipeRec(pNode):
    if pNode is None:
        return 0
    if pNode.left is None and pNode.right is None:
        return 1
    return _getSwipeRec(pNode.left) + _getSwipeRec(pNode.right) + 1


# operation 3
# This method searches for all players that are still
# on the premises and creates a list of such players.
def _onPremisesRec(pNode, ls):
    if pNode:
        _onPremisesRec(pNode.left, ls)
        if pNode.attrCtr % 2 == 1:
            ls.append(pNode.Pld)
        _onPremisesRec(pNode.right, ls)


# operation 4
# This method counts the number of times a particular
# player swiped today and if the player is currently in the hotel or outside.
def _checkEmpRec(pNode, Pld):
    p = search(pNode, Pld)
    if p is None:
        return "Player {} did not swipe today.\n".format(Pld)
    b = p.attrCtr % 2 == 1
    s = ""
    if b:
        s = "in"
    else:
        s = "outside"
    return "Player id {} swiped {} times today and is currently {} hotel.\n".format(Pld, p.attrCtr, s)


# operation 5
# This method generates the list of players
# who have swiped more than given number of times
def _frequentVisitorRec(pNode, freq):
    ls = []
    _inorder(pNode, ls, freq)
    return ls


# This method is called by _frequentVisitorRec method
def _inorder(pNode, ls, f):
    if pNode:
        _inorder(pNode.left, ls, f)
        if pNode.attrCtr >= f:
            ls.append("{},{}".format(pNode.Pld, pNode.attrCtr))
        _inorder(pNode.right, ls, f)


# operation 6
# This method prints the player ids in the range
# StartId to EndId and how often they have swiped and if they are inside or outside the hotel
def printRangePresent(pNode, start, end):
    ls = []
    inorder2(pNode, start, end, ls)
    return ls


# This method is called by printRangePresent method
def inorder2(pNode, start, end, ls):
    if pNode:
        inorder2(pNode.left, start, end, ls)
        if start <= pNode.Pld <= end:
            sl = ""
            if pNode.attrCtr % 2 == 1:
                sl = "in"
            else:
                sl = "out"
            ls.append("{},{},{}".format(pNode.Pld, pNode.attrCtr, sl))
        inorder2(pNode.right, start, end, ls)


# This method reads tags from the prompt file and executes them accordingly
# After that it stores the ans statement in the output file
def operation(pNode, str, filewrite):
    ls = str.split(":")
    if ls[0] == "onPremises":
        l = []
        _onPremisesRec(pNode, l)
        a = len(l)
        if a == 0:
            filewrite.write("No players present on premises.\n")
        else:
            filewrite.write("{} players still on premises.\n".format(a))
    elif ls[0] == "checkPlay":
        filewrite.write(_checkEmpRec(pNode, int(ls[1])))
    elif ls[0] == "freqVisit":
        filewrite.write("Players that swiped more than {} number of times today are:\n".format(int(ls[1])))
        tl = _frequentVisitorRec(pNode, int(ls[1]))
        for s in tl:
            filewrite.write(s + "\n")
    elif ls[0] == "range":
        filewrite.write("Range: {} to {}\n".format(int(ls[1]), int(ls[2])))
        filewrite.write("Player swipe:\n")
        tl = printRangePresent(pNode, int(ls[1]), int(ls[2]))
        for s in tl:
            filewrite.write(s + "\n")
    else:
        return "input not identified"


def promptoperation():
    root = _recordSwipeRes()
    fileWrite = open("outputPS12.txt", "w")
    fileWrite.write("Total number of players recorded today: {} \n".format(_getSwipeRec(root)))
    file = open("promptsPS12.txt", "r")
    l = list(file.readlines())
    for str in l:
        operation(root, str, fileWrite)
    file.close()
    fileWrite.close()


promptoperation()
