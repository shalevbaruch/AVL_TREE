def joinSTB(self, connecting_node, lst):  # STB == Small To Big - the case that self.height <= lst.height
    h1 = self.root.getHeight()
    temp = lst.root
    tmp_parent = temp.getParent()
    while temp.isRealNode() and temp.getHeight() > h1:  # going left on lst until temp.height <= self.height
        tmp_parent = temp
        temp = temp.getLeft()
    connecting_node.setLeft(self.root)  # creating connection between connecting_node and self.root
    self.root.setParent(connecting_node)
    if tmp_parent.isRealNode():  # if temp is not the root of lst
        connecting_node.setRight(temp)
        if temp.isRealNode():  # if temp is not virtual we need to set his parent
            temp.setParent(connecting_node)
        tmp_parent.setLeft(connecting_node)
        connecting_node.setParent(tmp_parent)
        self.root = lst.root
        self.lastitem = lst.lastitem
        self.size += lst.size + 1  # adding +1 because we deleted the connecting_node
        self.Fix_Up_Delete(
            connecting_node)  # need to do fix up to the root, while the fix up is same as the fix in delete

    else:  # temp is lst.root
        connecting_node.setRight(lst.root)
        lst.root.setParent(connecting_node)
        self.root = connecting_node
        self.lastitem = lst.lastitem
        self.size += lst.size + 1  # adding +1 because we deleted the connecting_node
        self.Fix_Up_Delete(connecting_node)  # maybe connecting_node need to be fixed
    return None


def joinBTS(self, connecting_node, lst):  # BTS == Big To Small - self.height > lst.height
    h1 = lst.root.getHeight()
    temp = self.root
    tmp_parent = temp.getParent()
    while temp.isRealNode() and temp.getHeight() > h1:  # going right on self until temp.height <= lst.height
        tmp_parent = temp
        temp = temp.getRight()
    connecting_node.setRight(lst.root)  # creating connection between connecting_node and lst.root
    lst.root.setParent(connecting_node)
    connecting_node.setLeft(temp)
    if temp.isRealNode():  # need to set parent if temp is not virtual
        temp.setParent(connecting_node)
    tmp_parent.setRight(connecting_node)
    connecting_node.setParent(tmp_parent)
    self.lastitem = lst.lastitem
    self.size += lst.size + 1  # adding +1 because we deleted the connecting_node
    self.Fix_Up_Delete(connecting_node)  # need to do fix up to the root, while the fix up is same as the fix in delete
    return


def concat(self, lst):
    h1 = self.root.getHeight()
    h2 = lst.root.getHeight()
    if not (lst.root.isRealNode()) or lst is None:  # if lst is empty we don't need to do anything
        return h1 + 1
    elif not (self.root.isRealNode()):  # if self is empty we need to convert self to lst
        self.root = lst.root
        self.lastitem = lst.lastitem
        self.firstitem = lst.firstitem
        self.size = lst.size
        return h2 + 1
    else:  # lst and self is not empty
        connecting_node = self.lastitem
        self.delete(self.size - 1)
        if self.root.getHeight() <= h2:  # calling to getHeight again because maybe after the deletion self.height <= h2
            if self.size == 0:  # if self had only one node at the start, we can convert self to lst and insert the node that we deleted at index 0
                self.root = lst.root
                self.lastitem = lst.lastitem
                self.firstitem = lst.firstitem
                self.insert(0, connecting_node.getValue())
                self.size = lst.size + 1
                return h2 + 1
            self.joinSTB(connecting_node, lst)  # case STB - Small To Big
        else:
            self.joinBTS(connecting_node, lst)  # case BTS - Big To Small
    return abs(h1 - h2)
