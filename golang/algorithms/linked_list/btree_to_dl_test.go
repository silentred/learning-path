package linkedList

import "testing"

func TestBtree(t *testing.T) {
	btree := createBinTree()
	printBinTree(btree.root)

	// node := newBinNode(1, nil, nil)
	// if node.left != nil {
	// 	fmt.Println("not nil")
	// } else {
	// 	fmt.Println("is nil")
	// }

	btree.convertToDlist()
	printDList(btree.root)
}
