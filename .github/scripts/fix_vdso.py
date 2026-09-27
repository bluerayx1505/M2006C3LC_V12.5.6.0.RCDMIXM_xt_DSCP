#!/usr/bin/env python3
import re
import sys

path = "kernel/arch/arm64/Makefile"

with open(path, "r") as f:
    content = f.read()

old_block = (
    "prepare: vdso_prepare\n"
    "vdso_prepare: prepare0\n"
    "\t$(Q)$(MAKE) $(build)=arch/arm64/kernel/vdso include/generated/vdso-offsets.h"
)

new_block = (
    "ifeq ($(KBUILD_EXTMOD),)\n"
    "prepare: vdso_prepare\n"
    "vdso_prepare: prepare0\n"
    "\t$(Q)$(MAKE) $(build)=arch/arm64/kernel/vdso include/generated/vdso-offsets.h\n"
    "endif"
)

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, "w") as f:
        f.write(content)
    print("Parche vdso_prepare aplicado correctamente.")
    sys.exit(0)

pattern = r"(prepare: vdso_prepare\s*\nvdso_prepare: prepare0\s*\n\t\$\(Q\)\$\(MAKE\).*vdso-offsets\.h)"
match = re.search(pattern, content)

if match:
    patched = "ifeq ($(KBUILD_EXTMOD),)\n" + match.group(1) + "\nendif"
    content = content.replace(match.group(1), patched)
    with open(path, "w") as f:
        f.write(content)
    print("Parche vdso_prepare aplicado (fallback).")
    sys.exit(0)

print("ERROR: No se pudo encontrar la sección vdso_prepare en arch/arm64/Makefile")
sys.exit(1)
