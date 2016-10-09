package linkedList

import "fmt"

type BinTree struct {
	root *BinNode
}

func (bt *BinTree) convertToDlist() {
	if bt.root == nil {
		return
	}

	root := convertBtreeToDlist(bt.root)
	for root.left != nil {
		root = root.left
	}

	bt.root = root
}

func printDList(root *BinNode) {
	fmt.Printf("%d ", root.data)
	if root.right != nil {
		printDList(root.right)
	}
}

func convertBtreeToDlist(root *BinNode) *BinNode {
	if root == nil {
		return nil
	}

	if root.left != nil {
		left := convertBtreeToDlist(root.left)
		for left.right != nil {
			left = left.right
		}

		left.right = root
		root.left = left
	}

	if root.right != nil {
		right := convertBtreeToDlist(root.right)
		for right.left != nil {
			right = right.left
		}

		right.left = root
		root.right = right
	}

	return root
}

type BinNode struct {
	data  int
	left  *BinNode
	right *BinNode
}

func newBinNode(data int, left, right *BinNode) *BinNode {
	return &BinNode{data, left, right}
}

func createBinTree() BinTree {
	sec := newBinNode(2, newBinNode(4, nil, nil), newBinNode(5, nil, nil))
	third := newBinNode(3, newBinNode(6, nil, nil), newBinNode(7, nil, nil))
	root := newBinNode(1, sec, third)
	return BinTree{root}
}

func printBinTree(root *BinNode) {
	if root == nil {
		return
	}

	if root.left != nil {
		printBinTree(root.left)
	}

	fmt.Printf(" %d %p - left %p \n", root.data, root, root.left)

	if root.right != nil {
		printBinTree(root.right)
	}
}
