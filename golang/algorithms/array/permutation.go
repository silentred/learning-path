package array

import "fmt"

func permuatation(str string) []string {
	var set []string

	if len(str) == 0 {
		set = addToSet(set, "")
		return set
	}

	firstChar := string(str[0])
	remaining := str[1:]

	permuatations := permuatation(remaining)

	fmt.Println(firstChar, remaining, len(remaining), permuatations, len(permuatations))
	for i := 0; i < len(permuatations); i++ {
		word := permuatations[i]
		//fmt.Println(i, word, len(word))

		for j := 0; j <= len(word); j++ {
			prefix := word[0:j]
			suffix := word[j:]
			set = addToSet(set, prefix+firstChar+suffix)

			// fmt.Println(word, prefix, suffix, set)
		}
	}

	return set
}

func addToSet(set []string, new string) []string {
	var found bool
	for i := 0; i < len(set); i++ {
		if set[i] == new {
			found = true
			break
		}
	}

	if !found {
		set = append(set, new)
	}

	return set
}
