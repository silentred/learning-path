# Memory Allocation

## Memory Layout
Each process has the same layout.
for example 32 bit OS.
Kernel (1G)
User Space (3G) {
    stack,
    Memory Mapping Segment, // file mappings and anonymous mappings
    heap,
    BSS segment, // uninitalized static variables, read-write (anonymous?)
    Data segment, // static var, read-write
    Text segment, // some parts of binary image, read + excute
}
