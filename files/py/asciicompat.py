#!/bin/python3
# This script is a modified version of a script by white-gecko from https://github.com/JasonN3/build-container-installer/issues/150
# It must be run at the end of an image build to ensure you won't get the error "Pathname can't be converted from UTF-8 to current locale" when installing from iso
# This script most likely won't help with installation at all unless rechunking is used
import subprocess
import os
from collections import defaultdict
# get installed packages
process = subprocess.run(["rpm", "-qa"], capture_output=True)
pkgs = process.stdout.decode("utf-8").split("\n")
pkg_files = {}

# get files in packages
for pkg in pkgs:
    process = subprocess.run(["rpm", "-ql", pkg], capture_output=True)
    pkg_files[pkg] = process.stdout.decode("utf-8").split("\n")

# make sure they can encode into ASCII
failed = defaultdict(list)
for pkg, files in pkg_files.items():
    for file in files:
        try:
            file.encode('ascii')
        except:
            failed[pkg].append(file)

print(dict(failed))

# if they can't, rename them so they can
for pkg, files in failed.items():
    for file in files:
        os.system(f"mv {file} {ascii(file).replace("\\u", "_u")}")
os.system("rm /usr/bin/asciicompat")
