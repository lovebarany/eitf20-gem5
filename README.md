# Lab files for EITF20 - Computer Architecture

This repository contains the provided files for the labs that use gem5 in the Computer Architecture course at Lund University.

**Current status**: WIP

## Directory structure
- /
    - labX/
        - configuration scripts (*.py)
        - benchmarks/
            - benchmark source code (*.c)
        - components/
            - custom components (*.py)
    - custom/
        - git patches for modules added to gem5 (*.patch)

## Custom modules for gem5

To add the modules to gem5, copy the *.patch file(s) to your base gem5 directory. Then type
```
git apply PATCH_NAME.patch
```
and rebuild gem5
