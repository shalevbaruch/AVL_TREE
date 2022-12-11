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
		if is_virtual == True:
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
		if self.left is AVLNode.virtual_node:
			return None
		return self.left

	"""returns the right child
    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

	def getRight(self):
		if self.right is AVLNode.virtual_node:
			return None
		return self.right

	"""returns the parent 
    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

	def getParent(self):
		if self.parent is AVLNode.virtual_node:
			return None
		return self.parent

	"""return the value
    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

	def getValue(self):
		if self is AVLNode.virtual_node:
			return None
		return self.value

	"""returns the height
    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

	def getHeight(self):
		return self.height

	"""sets left child
    @type node: AVLNode
    @param node: a node
    """

	def setLeft(self, node):
		self.left = node

	"""sets right child
    @type node: AVLNode
    @param node: a node
    """

	def setRight(self, node):
		self.right = node

	"""sets parent
    @type node: AVLNode
    @param node: a node
    """

	def setParent(self, node):
		self.parent = node

	"""sets value
    @type value: str
    @param value: data
    """

	def setValue(self, value):
		self.value = value
		return None

	"""sets the balance factor of the node
    @type h: int
    @param h: the height
    """

	def setHeight(self, h):
		self.height = h
		return None

	"""returns whether self is not a virtual node 
    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

	def isRealNode(self):
		return not (self is AVLNode.virtual_node)

	def getSize(self):
		if self.isRealNode()==False:
			return 0
		return self.size
	def setSize(self,s):
		self.size = s
	def get_BF(self):
		if self.isRealNode()==False:
			return 0
		else:
			return self.left.getHeight()-self.right.getHeight()

	def get_node_index(self, i):
			leftsize  = self.left.getSize()+1
			if i < leftsize:
				return self.left.get_node_index(i)
			elif i > leftsize:
				return self.right.get_node_index(i - leftsize)
			else:
				return self

	def Max(self):
		temp = self
		while temp.right.isRealNode():
			temp = temp.right
		return temp

	def min(self):
		temp = self
		while temp.left.isRealNode():
			temp = temp.left
		return temp

	def predecessor(self):
		if self.getLeft() is not None:
			pred = self.left.Max()
		else:
			temp = self
			pred = temp.parent
			while(temp.isRealNode() and temp == pred.left):
				temp = pred
				pred = temp.parent
		return pred
	def successor(self):
		if self.getRight() is not None:
			succ = self.right.min()
		else:
			temp = self
			succ = temp.parent
			while(temp.isRealNode() and temp == succ.right):
				temp = succ
				succ = temp.parent
		return succ

	def recalculate_node_attributes(self):
			self.height = max(self.left.getHeight(), self.right.getHeight()) + 1
			self.size = self.left.getSize() + self.right.getSize() + 1







"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):    ##possibly has to be fixed
		self.size = 0
		self.root = AVLNode(None)
		# add your fields here


	"""returns whether the list is empty
	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.size==0


	"""retrieves the value of the i'th item in the list
	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		return self.root.get_node_index(i+1).getValue()


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
		y = x.right
		x.right = y.left
		if y.getLeft() is not None:
			y.left.parent = x
		y.parent = x.parent
		if x.getParent() is None:
			self.root = y

		elif x == x.parent.left:
			x.parent.left = y

		else:
			x.parent.right = y

		y.left = x
		x.parent = y
		x.recalculate_node_attributes()
		y.recalculate_node_attributes()

	def right_rotate(self, x: AVLNode):
		y = x.left
		x.left = y.right
		if y.getRight() is not None:
			y.right.parent = x

		y.parent = x.parent
		if x.getParent() is None:
			self.root = y

		elif x == x.parent.right:
			x.parent.right = y

		else:
			x.parent.left = y

		y.right = x
		x.parent = y

		x.recalculate_node_attributes()
		y.recalculate_node_attributes()

	def insert(self, i, val):
		cnt=0
		node = AVLNode(val)
		if (i==self.size and self.empty()==False):
			temp1 = self.root.Max()
			temp1.setRight(node)
			node.setParent(temp1)
			par = temp1

		elif self.empty() and i ==self.size:
			self.root = node
			##self.root.setParent(AVLNode.virtual_node)
			par = AVLNode.virtual_node

		else:
			index_node = self.root.get_node_index(i+1)
			##if index_node.getLeft().isRealNode()==False:
			if index_node.getLeft() is None:
				index_node.setLeft(node)
				node.setParent(index_node)
				par = index_node
			else:
				pred = index_node.predecessor()
				pred.setRight(node)
				node.setParent(pred)
				par = pred
		##if node.parent.isRealNode()==False:
		if node.getParent() is None:
			self.root = node;
		temp = node
		self.size += 1
		while(par.isRealNode()):
			par.recalculate_node_attributes()
			##par.height = 1+max(par.left.getHeight(),par.right.getHeight())
			grand = par.parent
			if grand.get_BF()>=2 or grand.get_BF()<=-2:
				if par == grand.left:
					if temp == grand.left.left:
						self.right_rotate(grand)
						cnt+=1

					elif temp == grand.left.right:
						self.left_rotate(par)
						self.right_rotate(grand)
						cnt+=2


				elif par == grand.right:
					if temp == grand.right.right:
						self.left_rotate(grand)
						cnt+=1

					elif temp == grand.right.left:
						self.right_rotate(par)
						self.left_rotate(grand)
						cnt+=2
				##break we dont stop because we need to update size anyway
			par = par.parent
			temp = temp.parent
		return cnt

	def replace(self, u: AVLNode, v: AVLNode):
		if u.parent.isRealNode()==False:
			self.root = v
		elif u == u.parent.left:
			u.parent.left = v
		else:
			u.parent.right = v

		if v.isRealNode():
			v.parent = u.parent

	def Fix_Up_Delete(self, node:AVLNode):
		cnt = 0
		temp = node

		while temp.isRealNode():
			temp.recalculate_node_attributes()
			if temp.get_BF() <= -2 or temp.get_BF() >= 2:
				x = temp

				if x.left.height > x.right.height:
					Bigger_son = x.left
				else:
					Bigger_son = x.right

				if Bigger_son.left.height > Bigger_son.right.height:
					Bigger_grandson = Bigger_son.left

				elif Bigger_son.left.height < Bigger_son.right.height:
					Bigger_grandson = Bigger_son.right

				else:
					if Bigger_son == x.left:
						Bigger_grandson = Bigger_son.left
					else:
						Bigger_grandson = Bigger_son.right

				if Bigger_son == x.left:
					if Bigger_grandson == x.left.left:
						self.right_rotate(x)
						cnt+=1

					elif Bigger_grandson == x.left.right:
						self.left_rotate(Bigger_son)
						self.right_rotate(x)
						cnt+=2

				elif Bigger_son == x.right:
					if Bigger_grandson == x.right.right:
						self.left_rotate(x)
						cnt+=1

					elif Bigger_grandson == x.right.left:
						self.right_rotate(Bigger_son)
						self.left_rotate(x)
						cnt+=2

			temp = temp.parent
		return cnt









	"""deletes the i'th item in the list
	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		cnt=0
		node = self.root.get_node_index(i+1)
		##node = self.root.get_node_index(i + 1)
		if (i>=self.size):
			return -1
		##if node.getleft.isRealNode() == False:
		if node.getLeft() is None:
			self.replace(node, node.right)
			##node.recalculate_node_attributes()
			##node.right.recalculate_node_attributes()
			##self.size -= 1
			##if node.right.isRealNode():
			if node.getRight() is None:
				cnt += self.Fix_Up_Delete(node.right)

		##elif node.right.isRealNode()== False:
		elif node.getRight() is None:
			self.replace(node, node.left)
			##node.recalculate_node_attributes()
			##node.left.recalculate_node_attributes()
			if node.getLeft != None:
				cnt += self.Fix_Up_Delete(node.left)

		else:
			y = node.successor()
			if y.parent != node:
				self.replace(y, y.right)
				y.right = node.right
				y.right.parent = y
				##y.recalculate_node_attributes()
				##y.right.recalculate_node_attributes()


			self.replace(node, y)
			y.left = node.left
			y.left.parent = y
			##y.left.recalculate_node_attributes()
			##node.recalculate_node_attributes()
			if y.isRealNode():
				cnt += self.Fix_Up_Delete(y)
		self.size -= 1
		return cnt




	"""returns the value of the first item in the list
	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.size==0:
			return None
		else:
			return self.root.min().getValue()

	"""returns the value of the last item in the list
	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.size == 0:
			return None
		else:
			return self.root.Max().getValue()

	"""returns an array representing list 
	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		arr = [None for i in range(self.size)]
		Min = self.root.min()
		for j in range(self.size):
			arr[j] = Min.getValue()
			Min = Min.successor()
		return arr

	"""returns the size of the list 
	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.size

	"""sort the info values of the list
	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		arr = self.listToArray()
		arr.sort()
		i=0
		Min = self.root.min()
		for string in arr:
			Min.value = arr[i]
			Min = Min.successor()
			i+=1
		return self



	"""permute the info values of the list 
	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		temp = self.listToArray()
		random.shuffle(temp)
		Min = self.root.min()
		for j in range(self.size):
			Min.value = temp[j]
			Min = Min.successor()
		return self

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
		Min = self.root.min()
		index = -1
		for i in range(self.size):
			if Min.getValue() == val:
				index = i
				return index
			Min = Min.successor()
		return index




	"""returns the root of the tree representing the list
	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root

	def inorder(self, Root: AVLNode):
		if Root.isRealNode():
			self.inorder(Root.left)
			print(Root.getValue())
			self.inorder(Root.right)



tree = AVLTreeList()
arr = ["a","b", "c" , "d" , "e" , "f" , "g", "h"]
for i in range(8):
	tree.insert(i,arr[i])




##print(tree.search("D"))
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


