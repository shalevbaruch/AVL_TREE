# username - shalevbaruch,nethanel1
# id1      - 213070477
# name1    - Shalev Baruch
# id2      - 214194839
# name2    - Jonathan Nethanel


import random

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.
    @type value: str
    @param value: data of your node
    """
    virtual_node = None

    def __init__(self, value, is_virtual=False):
        if is_virtual:
            self.value = value
            self.is_virtual = True
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
            self.size = 0
            return
        if AVLNode.virtual_node is None:
            AVLNode.virtual_node = AVLNode("virtual", True)
        self.value = value
        self.is_virtual = False
        self.left = AVLNode.virtual_node
        self.right = AVLNode.virtual_node
        self.parent = AVLNode.virtual_node
        self.height = 0  # Balance factor
        self.size = 1

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if not (self.isRealNode()):
            return None
        return self.left

    """returns the right child
    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if not (self.isRealNode()):
            return None
        return self.right

    """returns the parent 
    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        if not (self.isRealNode()):
            return None
        return self.parent

    """return the value
    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        if not (self.isRealNode()):
            return None
        return self.value

    """returns the height
    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        if not (self.isRealNode()):
            return -1
        return self.height

    """sets left child
    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        if self.isRealNode():
            self.left = node
        return None

    """sets right child
    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        if self.isRealNode():
            self.right = node
        return None

    """sets parent
    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        if self.isRealNode():
            self.parent = node
        return None

    """sets value
    @type value: str
    @param value: data
    """

    def setValue(self, value):
        if self.isRealNode():
            self.value = value
        return None

    """sets the balance factor of the node
    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        if self.isRealNode():
            self.height = h
        return None

    """returns whether self is not a virtual node 
    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return not (self is AVLNode.virtual_node)

    def getSize(self):
        return self.size

    def setSize(self, s):
        if self.isRealNode():
            self.size = s
        return None

    def get_BF(self):
        if not self.isRealNode():
            return 0
        else:
            return self.getLeft().getHeight() - self.getRight().getHeight()

    def get_node_index(self, i):  # like select(i)
            ##if self.getLeft() is None:
            ##return self
            if not(self.getLeft().isRealNode()):
                leftsize = 1
            else:
                leftsize = self.getLeft().getSize() + 1
            if i < leftsize:
                return self.getLeft().get_node_index(i)
            elif i > leftsize:
                if not(self.getRight().isRealNode()):
                    return self
                return self.getRight().get_node_index(i - leftsize)
            else:
                return self

    def Max(self):  # right all the way
        temp = self
        while temp.right.isRealNode():
            temp = temp.getRight()
        return temp

    def Min(self):  # left all the way
        temp = self
        while temp.left.isRealNode():
            temp = temp.left
        return temp

    def predecessor(self):
        if self.getLeft().isRealNode():
            pred = self.getLeft().Max()
        else:
            temp = self
            pred = temp.getParent()
            while pred.isRealNode() and temp == pred.getLeft():
                temp = pred
                pred = temp.getParent()
        return pred

    def successor(self):
        if self.getRight().isRealNode():
            succ = self.getRight().Min()
        else:
            temp = self
            succ = temp.getParent()
            while succ.isRealNode() and temp == succ.getRight():
                temp = succ
                succ = temp.getParent()
        return succ

    def recalculate_node_attributes(self):
        self.height = max(self.getLeft().getHeight(), self.getRight().getHeight()) + 1
        self.size = self.getLeft().getSize() + self.getRight().getSize() + 1


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.size = 0
        self.root = AVLNode(None)
        self.lastitem = AVLNode(None)
        self.firstitem = AVLNode(None)

    # add your fields here

    """returns whether the list is empty
    @rtype: bool
    @returns: True if the list is empty, False otherwise

    """

    def shuffler(self, arr, n):

        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    def empty(self):
        return self.size == 0

    """retrieves the value of the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        if i >= self.length():
            return -1
        return self.root.get_node_index(i + 1).getValue()

    """inserts val at position i in the list
    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def left_rotate(self, x: AVLNode):
        y = x.getRight()
        x.setRight(y.getLeft())
        if y.getLeft().isRealNode():
            y.getLeft().setParent(x)
        y.setParent(x.getParent())
        if not (x.getParent().isRealNode()):
            self.root = y

        elif x == x.getParent().getLeft():
            x.getParent().setLeft(y)

        else:
            x.getParent().setRight(y)

        y.setLeft(x)
        x.setParent(y)
        x.recalculate_node_attributes()
        y.recalculate_node_attributes()

    def right_rotate(self, x: AVLNode):
        y = x.getLeft()
        x.setLeft(y.getRight())
        if y.getRight().isRealNode():
            y.getRight().setParent(x)

        y.setParent(x.getParent())
        if not (x.getParent().isRealNode()):
            self.root = y

        elif x == x.getParent().getRight():
            x.getParent().setRight(y)

        else:
            x.getParent().setLeft(y)

        y.setRight(x)
        x.setParent(y)

        x.recalculate_node_attributes()
        y.recalculate_node_attributes()


    def insert(self, i, val):
        if i >= self.size + 1:
            return -1
        cnt = 0
        node = AVLNode(val)
        if i == self.size and not (self.empty()):
            temp1 = self.lastitem
            temp1.setRight(node)
            node.setParent(temp1)
            self.lastitem = node
            par = temp1

        elif self.empty() and i == self.size:
            self.root = node
            self.lastitem = node
            self.firstitem = node
            par = AVLNode.virtual_node

        else:
            if (i==0):
                index_node = self.firstitem
            else:
                index_node = self.root.get_node_index(i + 1)
            if not (index_node.getLeft().isRealNode()):
                index_node.setLeft(node)
                node.setParent(index_node)
                par = index_node
                if i == 0:
                    self.firstitem = node
            else:
                pred = index_node.predecessor()
                pred.setRight(node)
                node.setParent(pred)
                par = pred
        if not (node.getParent().isRealNode()):
            self.root = node
        temp = node
        self.size += 1
        while par.isRealNode():
            par.recalculate_node_attributes()
            grand = par.getParent()
            if grand.get_BF() >= 2 or grand.get_BF() <= -2:
                if par == grand.getLeft():
                    if temp == grand.getLeft().getLeft():
                        self.right_rotate(grand)
                        cnt += 1

                    elif temp == grand.getLeft().getRight():
                        self.left_rotate(par)
                        self.right_rotate(grand)
                        cnt += 2

                elif par == grand.getRight():
                    if temp == grand.getRight().getRight():
                        self.left_rotate(grand)
                        cnt += 1

                    elif temp == grand.getRight().getLeft():
                        self.right_rotate(par)
                        self.left_rotate(grand)
                        cnt += 2
            par = par.getParent()
            temp = temp.getParent()
        return cnt

    def replace(self, x: AVLNode, y: AVLNode):
        if not x.getParent().isRealNode():
            self.root = y
        elif x == x.getParent().getLeft():
            x.getParent().setLeft(y)
        else:
            x.getParent().setRight(y)

        if y.isRealNode():
            y.setParent(x.getParent())
        ##x.setLeft(AVLNode.virtual_node)
        ##x.setRight(AVLNode.virtual_node)
        ##x.setParent(AVLNode.virtual_node)
        ##y.recalculate_node_attributes()

    def Fix_Up_Delete(self, node: AVLNode):
        cnt = 0
        temp = node

        while temp.isRealNode():
            temp.recalculate_node_attributes()
            if temp.get_BF() <= -2 or temp.get_BF() >= 2:
                x = temp

                if x.getLeft().getHeight() > x.getRight().getHeight():
                    Bigger_son = x.getLeft()
                else:
                    Bigger_son = x.getRight()

                if Bigger_son.getLeft().getHeight() > Bigger_son.getRight().getHeight():
                    Bigger_grandson = Bigger_son.getLeft()

                elif Bigger_son.getLeft().getHeight() < Bigger_son.getRight().getHeight():
                    Bigger_grandson = Bigger_son.getRight()

                else:
                    if Bigger_son == x.getLeft():
                        Bigger_grandson = Bigger_son.getLeft()
                    else:
                        Bigger_grandson = Bigger_son.getRight()

                if Bigger_son == x.getLeft():
                    if Bigger_grandson == x.getLeft().getLeft():
                        self.right_rotate(x)
                        cnt += 1

                    elif Bigger_grandson == x.getLeft().getRight():
                        self.left_rotate(Bigger_son)
                        self.right_rotate(x)
                        cnt += 2

                elif Bigger_son == x.getRight():
                    if Bigger_grandson == x.getRight().getRight():
                        self.left_rotate(x)
                        cnt += 1

                    elif Bigger_grandson == x.getRight().getLeft():
                        self.right_rotate(Bigger_son)
                        self.left_rotate(x)
                        cnt += 2

            temp = temp.getParent()
        return cnt

    """deletes the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if (self.length() == 1):
            self.lastitem = None
            self.firstitem = None
            self.size = 0
            self.root = None
            return 0
        cnt = 0
        node = self.root.get_node_index(i + 1)
        if i == self.size - 1:
            self.lastitem = self.lastitem.predecessor()
        if i == 0:
            self.firstitem = self.firstitem.successor()
        if i >= self.size:
            return -1
        if (self.size == 2):
            self.firstitem = self.lastitem
        if not(node.getLeft().isRealNode()):
            self.replace(node, node.getRight())
            node.recalculate_node_attributes()
            if not(node.getRight().isRealNode()):
                cnt += self.Fix_Up_Delete(node.getRight())
        elif not(node.getRight().isRealNode()):
            self.replace(node, node.getLeft())
            if node.getLeft().isRealNode():
                cnt += self.Fix_Up_Delete(node.getLeft())

        else:
            y = node.successor()
            if y.getParent() != node:
                self.replace(y, y.getRight())
                y.right = node.getRight()
                y.getRight().setParent(y)

            self.replace(node, y)
            y.setLeft(node.getLeft())
            y.getLeft().setParent(y)
            if y.isRealNode():
                cnt += self.Fix_Up_Delete(y)
        self.size -= 1
        return cnt

    """returns the value of the first item in the list
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.size == 0:
            return None
        else:
            return self.firstitem.getValue()

    """returns the value of the last item in the list
    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.size == 0:
            return None
        else:
            return self.lastitem.getValue()

    """returns an array representing list 
    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        arr = [None for i in range(self.size)]
        minimum = self.firstitem
        for j in range(self.size):
            arr[j] = minimum.getValue()
            minimum = minimum.successor()
        return arr

    """returns the size of the list 
    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    def SORT(self, array):
        if len(array) > 1:
            r = len(array) // 2
            L = array[:r]
            M = array[r:]
            self.SORT(L)
            self.SORT(M)
            i = j = k = 0
            while i < len(L) and j < len(M):
                if L[i] < M[j]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = M[j]
                    j += 1
                k += 1

            # When we run out of elements in either L or M,
            # pick up the remaining elements and put in A[p..r]
            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1

            while j < len(M):
                array[k] = M[j]
                j += 1
                k += 1

    """sort the info values of the list
    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        arr = self.listToArray()
        self.SORT(arr)
        i = 0
        root2 = self.cloneBinaryTree(self.root)
        tree2 = AVLTreeList()
        tree2.setTree(root2)
        minimum = tree2.firstitem
        for string in arr:
            minimum.value = arr[i]
            minimum = minimum.successor()
            i += 1
        return tree2

    """permute the info values of the list 
    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        temp = self.listToArray()
        random.shuffle(temp)
        self.shuffler(temp, self.size)
        root2 = self.cloneBinaryTree(self.root)
        tree2 = AVLTreeList()
        tree2.setTree(root2)
        minimum = tree2.firstitem
        for inti in temp:
            minimum.value = inti
            minimum = minimum.successor()
        return tree2

    """concatenates lst to self
    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        return None

    """searches for a *value* in the list
    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        minimum = self.firstitem
        index = -1
        for i in range(self.size):
            if minimum.getValue() == val:
                index = i
                return index
            minimum = minimum.successor()
        return index

    def cloneBinaryTree(self, curr: AVLNode):
        if not curr.isRealNode():
            return
        root_copy = AVLNode(curr.getValue())
        root_copy.setSize(curr.getSize())
        root_copy.setHeight(curr.getHeight())
        if not(curr.getLeft().isRealNode()):
            root_copy.setLeft(AVLNode.virtual_node)
        else:
            root_copy.setLeft(self.cloneBinaryTree(curr.getLeft()))
        root_copy.getLeft().setParent(root_copy)
        if not(curr.getRight().isRealNode()):
            root_copy.setRight(AVLNode.virtual_node)
        else:
            root_copy.setRight(self.cloneBinaryTree(curr.getRight()))
        root_copy.getRight().setParent(root_copy)
        return root_copy

    def setTree(self, Root: AVLNode):
        self.root = Root
        self.size = Root.getSize()
        self.lastitem = Root.Max()
        self.firstitem= Root.Min()

    """returns the root of the tree representing the list
    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if self.empty():
            return None
        return self.root


    def inorder(self, Root: AVLNode):
        if Root.isRealNode():
            self.inorder(Root.getLeft())
            print(Root.getValue())
            self.inorder(Root.getRight())
    def testq1Part1(self):
        print("question 1")
        print("part 1")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n):
                k = random.randint(0, tree.length())
                count += tree.insert(k, str(k))
            print("count for i =", i, " is:", count)
    def testq1Part2(self):
        print("part 2")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n):
                k = random.randint(0, tree.length())
                tree.insert(k, str(k))
            for j in range(0, n):
                k = random.randint(0, tree.length() - 1)
                count += tree.delete(k)
            print("count for i =", i, " is:", count)

    def testq1Part3(self):
        print("part 3")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n // 2):
                k = random.randint(0, tree.length())
                count += tree.insert(k, str(k))
            for j in range(0, n // 2):
                if j % 2 == 0:
                    k = random.randint(0, tree.length() - 1)
                    count += tree.delete(k)
                else:
                    k = random.randint(0, tree.length())
                    count += tree.insert(k, str(k))
            print("count for i =", i, " is:", count)
    def testq2Part1(self):
        print("question 2")
        print("part 3")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n):
                k = random.randint(0, tree.length())
                count += tree.insert(0, str(k))
            print("count for i =", i, " is:", count)
    def testq2Part2(self):
        print("part 3")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n):
                k = random.randint(0, tree.length())
                count += tree.insert(k, str(k))
            print("count for i =", i, " is:", count)

    def testq2Part3(self):
        print("part 3")
        count = 0
        for i in range(1, 11):
            tree = AVLTreeList()
            n = 1500 * (2 ** i)
            for j in range(0, n):
                k = random.randint(0, tree.length())
                count += tree.insert(tree.length(), str(k))

##tree = AVLTreeList()
##tree2 = AVLTreeList()
##tree2.insert(0,"0")
##tree2.insert(1,"1")
##tree2.insert(0,"2")
##print(tree2.listToArray())

##tree.testq1Part1()
##tree.testq1Part2()
##tree.testq1Part3()
##n = 50
##mylist = []
##mylist2 = []
##for j in range(0, n):
##    k = random.randint(0, tree.length())
##    mylist2.insert(j,k)
##    mylist.insert(k,str(j))
##    tree.insert(k, str(j))
##print("correct list")
##print(mylist)
##print("my list")
##print(tree.listToArray())
##print("indexes")
##print(mylist2)
##print(tree.first())
##print(tree.last())

#3arr = ["w","a","c","z","d"]
##for i in range(5):
##	tree.insert(i,arr[i])
##for i in range(5):
##	tree.delete(0)
##for i in range(4):
##	tree.delete(0)
##tree.delete(0)
##tree.delete(0)
##tree.delete(0)
##tree.delete(1)
##tree.delete(0)
##print(tree.first())
##print(tree.last())
##print(tree.size)
##tree.delete(0)
##tree.inorder(tree.sort().root)
##tree.inorder(tree.permutation().getRoot())



##tree2 = tree.permutation()
##tree2.inorder(tree2.root)
##print (tree.inorder(tree.root))
##print (tree.inorder(tree.root))
##print (tree.inorder(tree.root))
##tree.delete(0)
##print(tree.first())
##print(tree.retrieve(2))
##tree2 = AVLTreeList()
##tree2.testq1()


#print(tree.search("d"))
##cnt = tree.insert(3,"F")
##print(tree.delete(3))
##print(tree.insert(4,"A"))
##print(tree.delete(4))
##tree.inorder(tree.getRoot())
##tree.inorder(tree.permutation().getRoot())
##print(cnt)
##print (tree.retrieve(1))

##print(tree.search("A"))
##tree.insert(0,"C")
##tree.inorder(tree.getRoot())
##tree.delete(0)
##tree.inorder(tree.sort().getRoot())
