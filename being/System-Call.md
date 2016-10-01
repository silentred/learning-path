# System Call

## File

### fdatasync

```
#include <unistd.h>
int fsync(int fd);
int fdatasync(int fd);
```
fsync() transfers ("flushes") all modified in-core data of (i.e., modified buffer cache pages for) the file referred to by the file descriptor fd to the disk device (or other permanent storage device) so that all changed information can be retrieved even after the system crashed or was rebooted. This includes writing through or flushing a disk cache if present. The call blocks until the device reports that the transfer has completed. It also flushes metadata information associated with the file (see stat(2)).

Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk. For that an explicit fsync() on a file descriptor for the directory is also needed.

fdatasync() is similar to fsync(), but does not flush modified metadata unless that metadata is needed in order to allow a subsequent data retrieval to be correctly handled. For example, changes to st_atime or st_mtime (respectively, time of last access and time of last modification; see stat(2)) do not require flushing because they are not necessary for a subsequent data read to be handled correctly. On the other hand, a change to the file size (st_size, as made by say ftruncate(2)), would require a metadata flush.

The aim of fdatasync() is to reduce disk activity for applications that do not require all metadata to be synchronized with the disk.


### sync_file_range

```
#define _GNU_SOURCE         /* See feature_test_macros(7) */
#include <fcntl.h>
int sync_file_range(int fd, off64_t offset, off64_t nbytes, unsigned int flags);
```

sync_file_range() permits fine control when synchronizing the open
file referred to by the file descriptor fd with disk.

offset is the starting byte of the file range to be synchronized.
nbytes specifies the length of the range to be synchronized, in
bytes; if nbytes is zero, then all bytes from offset through to the
end of file are synchronized.  Synchronization is in units of the
system page size: offset is rounded down to a page boundary;
(offset+nbytes-1) is rounded up to a page boundary.


Warning:
This system call is extremely dangerous and should not be used in
portable programs.  None of these operations writes out the file's
metadata.  Therefore, unless the application is strictly performing
overwrites of already-instantiated disk blocks, there are no
guarantees that the data will be available after a crash.  There is
no user interface to know if a write is purely an overwrite.  On
filesystems using copy-on-write semantics (e.g., btrfs) an overwrite
of existing allocated blocks is impossible.  When writing into
preallocated space, many filesystems also require calls into the
block allocator, which this system call does not sync out to disk.
This system call does not flush disk write caches and thus does not
provide any data integrity on systems with volatile disk write
caches.

### fallocate

```
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <fcntl.h>
int fallocate(int fd, int mode, off_t offset/"", off_t " len ");
```

This is a nonportable, Linux-specific system call. For the portable, POSIX.1-specified method of ensuring that space is allocated for a file, see posix_fallocate(3).
fallocate() allows the caller to directly manipulate the allocated disk space for the file referred to by fd for the byte range starting at offset and continuing for len bytes.

The mode argument determines the operation to be performed on the given range. Details of the supported operations are given in the subsections below.
