#!/usr/bin/env python3
#
# lobster-trlc-system-test - Extract tracing tags for LOBSTER
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This component of TRLC program is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
# pylint: disable=invalid-name
import os
import sys
from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write
from trlc.trlc import Source_Manager
from trlc.errors import Message_Handler

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET   = "system-tests.lobster"

def process(test_dir, mapping):
    assert os.path.isdir(test_dir)
    assert isinstance(mapping, dict)
    tag_file = os.path.join(test_dir, "tracing")
    testname = os.path.basename(test_dir)
    item = Activity(
        tag       = Tracing_Tag(namespace = "trlc-st",
                                tag       = testname),
        location  = File_Reference(filename = test_dir),
        framework = "TRLCST",
        kind      = "Test Directory")
    include_test = False
    if os.path.isfile(tag_file):
        include_test = True
        with open(tag_file, "r", encoding="UTF-8") as fd:
            tags = [Tracing_Tag(namespace = "req",
                                tag       = line.strip())
                    for line in fd.read().splitlines()
                    if line.strip()]
        for tag in tags:
            item.add_tracing_target(tag)
    if testname.startswith("rbt-"):
        include_test = True
        components = testname[4:].lower().split("-")
        if len(components) >= 2:
            try:
                int(components[-1])
                components.pop()
            except ValueError:
                pass
        requirement = mapping.get("-".join(components),
                                  "_".join(item.capitalize()
                                           for item in components))
        item.add_tracing_target(
            Tracing_Tag(namespace = "req",
                        tag       = "req.%s" % requirement))
    if include_test:
        return [item]
    else:
        # We don't need to know about untraced regression tests
        return []


def main(lobster_folder):
    sm = Source_Manager(mh = Message_Handler(),
                        lint_mode   = False,
                        parse_trlc  = True,
                        verify_mode = False)

    filename = os.path.join(SCRIPT_DIR, 'lobster/tools')
    sm.register_directory(filename)
    stab = sm.process()
    pkg_req = stab.lookup_assuming(sm.mh, "req")
    mapping = {}
    for item in pkg_req.symbols.iter_record_objects():
        mapping[item.name.lower().replace("_", "-")] = item.name

    items = []
    for dirent in sorted(os.scandir(SCRIPT_DIR),
                         key=lambda de: de.name):
        if dirent.is_dir() and dirent.name == lobster_folder:
            if dirent.name == "htmlcov":
                continue
            items += process(dirent.name, mapping)

    with open(TARGET, "w", encoding="UTF-8") as fd:
        lobster_write(fd, Activity, "lobster-trlc-system-test", items)

    print("Written %u items to %s" % (len(items), TARGET))
    return 0


if __name__ == "__main__":
    lobster_folder = sys.argv[1]
    sys.exit(main(lobster_folder))