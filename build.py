from glob import glob
import os
import pathlib
import re

import pybind11
from pybind11.setup_helpers import ParallelCompile, naive_recompile

__version__ = "3.3.28"  # <<FORCE_BUMP>>

from setuptools import Extension

ParallelCompile(
    "NPY_NUM_BUILD_JOBS",
    needs_recompile=naive_recompile,
).install()
debug_mode = os.environ.get("DEBUG_MODE", "false").lower() == "true"
version_info = os.environ.get("VERSION_INFO", __version__)

# Conditional compilation flags
extra_compile_args = []
if debug_mode:
    extra_compile_args.append("-DDEBUG_MODE")


def find_replace(file_list, find, replace, file_pattern):
    for file in [x for x in file_list if re.match(file_pattern, x)]:
        with open(file) as file_r:
            s = file_r.read()
        s = s.replace(find, replace)
        with open(file, "w") as file_w:
            file_w.write(s)


__version__ = "3.0.4"  # <<FORCE_BUMP>>
with open("filet/__init__.py") as f:
    while line := f.readline():
        if "__version__" in line:
            __version__ = eval(line.split("=").pop().strip())

os.environ["VERSION_INFO"] = __version__

pkg_path = "filet"
external_path = "lib"
path = "cpputils"
files = [
    f
    for f in [*glob(f"{path}/*/**", recursive=True), *glob(f"{path}/*", recursive=True)]
    if "test" not in f
    if os.path.splitext(f)[1] == ".cpp"
]

ext_paths = [external_path, pybind11.get_include(), f"{external_path}/rapidjson/include"]

long_description = pathlib.Path("README.rst").read_text()


def build(setup_kwargs):
    ext_modules = [
        Extension(
            "filet._cpputils",
            [*files],
            include_dirs=[path, *ext_paths],  cxx_std=11,
            extra_compile_args=extra_compile_args,
        ),
    ]
    setup_kwargs.update(
        {
            "long_description": long_description,
            "ext_modules": ext_modules,
            # "build_ext": build_ext,
            "long_description_content_type": "text/x-rst",
            "zip_safe": False,
        }
    )
