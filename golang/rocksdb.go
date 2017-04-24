package main

import (
	"log"

	"github.com/siddontang/ledisdb/config"
	"github.com/siddontang/ledisdb/store"
)

func main() {
	cfg := config.NewConfigDefault()
	cfg.DBName = "rocksdb"
	db, err := store.Open(cfg)
	if err != nil {
		log.Fatal(err)
	}
	db.Put([]byte("foo"), []byte("bar"))
}

//CGO_CFLAGS="-I/usr/local/rocksdb" CGO_CXXFLAGS="-I/usr/local/rocksdb/include" CGO_LDFLAGS="-I/usr/local/rocksdb/lib -lrocksdb" LD_LIBRARY_PATH="/usr/local/rocksdb/lib" DYLD_LIBRARY_PATH="/usr/local/rocksdb/lib" go build -o main -tags "rocksdb"

//CGO_CFLAGS="-I/usr/local/rocksdb" CGO_CXXFLAGS="-I/usr/local/rocksdb/include" CGO_LDFLAGS="-I/usr/local/rocksdb/lib -lrocksdb" go build -o main -tags "rocksdb"
