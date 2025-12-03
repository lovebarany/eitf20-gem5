# Lab files for EITF20 - Computer Architecture

This repository contains the provided files for the labs that use gem5 in the Computer Architecture course at Lund University.

**Current status**:
- lab2: FINISHED
- lab4: WIP

## Directory structure
- /
    - labX/
        - configuration scripts (*.py)
        - components/
            - custom components (*.py)
    - custom/
        - git patches for modules added to gem5 (*.patch)
    - workloads/
        - files used to create workloads

## Custom modules for gem5

To add the modules to gem5, copy the *.patch file(s) to your base gem5 directory. Then type
```
git apply PATCH_NAME.patch
```
and rebuild gem5.

## Workloads

You will need to compile all workloads, which can be done with the makefile `workloads/Makefile`. You need to specify where the gem5 repository is located. Also note that you need to build m5 as well.

Then, you will have to update `workloads/local-resources.json` with the path to the binaries, and the md5sum of the binaries. Finally, you will need to append `workloads/local-resources.json` to the gem5 resource path.
