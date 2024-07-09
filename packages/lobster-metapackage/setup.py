#!/usr/bin/env python3

import os
import re
import sys
import setuptools
import glob

#from lobster import version
VERSION_TUPLE = (0, 9, 17)
VERSION_SUFFIX = "dev"

LOBSTER_VERSION = ("%u.%u.%u" % VERSION_TUPLE) + \
    ("-%s" % VERSION_SUFFIX if VERSION_SUFFIX else "")

gh_root = "https://github.com"
gh_project = "bmw-software-engineering/lobster"

with open("README.md", "r") as fd:
    long_description = fd.read()

with open("requirements", "r") as fd:
    package_requirements = [line
                            for line in fd.read().splitlines()
                            if line.strip()]

# For the readme to look right on PyPI we need to translate any
# relative links to absolute links to github.
fixes = []
for match in re.finditer(r"\[(.*)\]\((.*)\)", long_description):
    if not match.group(2).startswith("http"):
        fixes.append((match.span(0)[0], match.span(0)[1],
                      "[%s](%s/%s/blob/main/%s)" % (match.group(1),
                                                    gh_root,
                                                    gh_project,
                                                    match.group(2))))

for begin, end, text in reversed(fixes):
    long_description = (long_description[:begin] +
                        text +
                        long_description[end:])

project_urls = {
    "Bug Tracker"   : "%s/%s/issues" % (gh_root, gh_project),
    "Documentation" : "%s/pages/%s/" % (gh_root, gh_project),
    "Source Code"   : "%s/%s"        % (gh_root, gh_project),
}

packages = ["bmw-lobster-core>=%s" % LOBSTER_VERSION]
for dirname in glob.glob("../lobster-tool-*"):
    packages.append("bmw-%s>=%s" % (os.path.basename(dirname),
                                    LOBSTER_VERSION))
packages += package_requirements

setuptools.setup(
    name="bmw-lobster",
    version=LOBSTER_VERSION,
    author="Bayerische Motoren Werke Aktiengesellschaft (BMW AG)",
    author_email="philipp.wullstein-kammler@bmw.de",
    description="Metapackage to install all LOBSTER Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=project_urls["Source Code"],
    project_urls=project_urls,
    license="GNU Affero General Public License v3",
    packages=[],
    install_requires=packages,
    python_requires=">=3.7, <4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Documentation",
        "Topic :: Software Development",
    ]
)
