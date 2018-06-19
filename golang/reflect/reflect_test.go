package reflect_test

import (
	"reflect"
	"strings"
	"testing"
)

type A struct {
	Name   string
	Age    int
	Job    Job
	Labels map[string]string
}

type Job struct {
	Title  string
	Labels map[string]string
}

func GetByPath(path []string, v interface{}) reflect.Value {
	val := reflect.ValueOf(v)
	for _, field := range path {
		val = GetField(field, val)
	}
	return val
}

func GetField(field string, v interface{}) reflect.Value {
	var val reflect.Value
	var ok bool
	if val, ok = v.(reflect.Value); !ok {
		val = reflect.ValueOf(v)
	}

	if val.Kind() == reflect.Ptr {
		val = val.Elem()
	}

	if val.Kind() == reflect.Map {
		return val.MapIndex(reflect.ValueOf(field))
	}

	if val.Kind() == reflect.Struct {
		t := val.Type()
		for i := 0; i < val.NumField(); i++ {
			if t.Field(i).Name == field {
				return val.Field(i)
			}
		}
	}

	return val
}

func TestReflect(t *testing.T) {
	a := A{
		Name: "jason",
		Age:  18,
		Labels: map[string]string{
			"a": "b",
			"c": "d",
		},
		Job: Job{
			Title: "worker",
			Labels: map[string]string{
				"a": "b",
				"c": "d",
			},
		},
	}

	v := GetField("Name", a)
	t.Logf("%+v", v)

	v = GetField("Age", a)
	t.Logf("%#v", v.Int())

	v2 := GetByPath([]string{"Labels", "c"}, a)
	t.Logf("%+v", v2)

	v3 := GetByPath([]string{"Job", "Labels", "a"}, a)
	t.Logf("%+v", v3)

	s := strings.Split("", ",")
	t.Logf("%+v, %+v", len(s), s)
}
