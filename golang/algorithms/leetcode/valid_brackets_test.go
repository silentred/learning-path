package leetcode

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBrackets(t *testing.T) {
	tbl := []struct {
		str   string
		valid bool
	}{
		{"{{[()]}}", true},
		{"{}(){}[]{([])}", true},
		{"{()}(]{}[{}]", false},
		{"){", false},
	}

	for _, item := range tbl {
		assert.Equal(t, item.valid, isValid(item.str))
	}
}
