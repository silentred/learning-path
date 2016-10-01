# Haystack Note

## Overview
Haystack Store, Directory, Cache

Store: physical volumes

Directory: map( logical volumes => physical volumes )
one physical volume could map to multiple logical volumes, for redundancy.

Cache: internal CDN


## Directory
Four main functions:

1. map logical volumes to physical volumes
2. load balances writes across logical volumes and reads across physical volumes
3. determine a request to be handled by CDN or Cache
4. identify if a store is read-only (reach storage capacity or be set manually)

when a new machine is added in, it is write-enabled. when a Store reaches its capacity, it is marked as read-only.
when a Store lost data, it should be removed from Directory. Then a new Store should be braught online.

## Cache

receives HTTP request(from CDN or browser), if cannot respond, fetch photo from Stores.
cache phone only when:
a. request is from User, not CDN
b. the photo is fetched from write-enabled Store

reason for a:
post-CDN caching is ineffective?

reason for b:
photo is most heavily accessed after it is uploaded. 

## Store

A physical volume is a very large file (100 GB), 
//not sure ?? located at /hay/haystack_<logical_volume_id>

Needle struct:
Field   Comment

Header  magic number
Cookie  random number to mitigate brute force lookups // no need
Key     64-bit id
Alternate key   32-bit id
Flags   if deleted
Size    data size
Data    actual data
Footer  magic number for recovery
Data Checksum   check integrity
Padding needle size is aligned to 8 bytes

one open fd for each physical volume
in-memory mapping of photo_id to file metadata (file, offset, size in byte)
a Store machine = one physical volume (has one superblock)
map [key, alternate key] => (needle's flags, size, offset, )

### Read

Cache supplies logical volume id, key, alternate key, and cookie to the Store machine
The cookie’s value is randomly assigned by and stored in the Directory at the time that the photo is uploaded

### Write

provides logical volume id, key, alternate key, cookie, and data to Store machines

append-only

disallow overwritting needle. photos can only be modified by adding an updated needle with the same key and alternate key. 

If the new needle is written to a different logical volume than the original, the Directory updates its application metadata and future requests will never fetch the older version. 
If the new needle is written to the same logical volume, then Store machines append the new needle to the same corresponding physical volumes.

### Delete

set flag in metadata and volume file
the space of deleted needle is lost for moment, the compacting action will reclaim the space.

### Index File

When we write a new photo the Store machine synchronously appends a needle to the end of the volume file and asynchronously appends a record to the index file. 

When we delete a photo, the Store machine synchronously sets the flag in that photo’s needle without updating the index file.

Two effects:
1. needles can exist without corresponding index records. The needle is called orphan
2. index records do not reflect deleted photos

Index Struct:
Key     
Alternate Key
Flags
Offset
Size

the Store machine now initializes its in-memory mappings using only the index files.
Index records do not reflect deleted photos. After a Store machine reads the entire needle for a photo, that machine can then inspect the deleted flag.

### Filesystem

the Store machines should use a filesystem that does not need much memory to be able to perform random seeks within a large file quickly.

XFS has 2 advantages:
1, the blockmaps for several contiguous large files can be small enough to be stored in main memory. 
2, XFS provides efficient file preallocation, mitigating fragmentation and reining in how large block maps can grow.

## Recovery from failure

failure types:
faulty hard drives, misbehaving RAID controllers, bad motherboards, etc.

work in two aspect:
detection and repair

### Pitchfork

periodically 
1. test connection to Store machine
2. try to read data from Store machine

if Store constently fails health checks:
pitchfork mark all the logical volumes in that Store as read-only

bulk sync: reset data of a Store machine using vulume files from a replica.
rarely used.

## Optimizations

### Compaction

copying needles into a new file while skipping any duplicate or deleted entries. 
During compaction, deletes go to both files.
In the end, it blocks all modifications to the volume, and swaps old and new volume in metadata.

### Saving more memory
remove flags, cookie from index struct.
So, the metadata contains:
key uint64,
offset uint32,
size uint32

### Batch upload











