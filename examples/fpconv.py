#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import sys
import logging
import vcd
import csv
from pathlib import Path


class FPConvWatcher(vcd.VCDWatcher):
    def __init__(self, parser, **kwds):
        super().__init__(parser, **kwds)
        self.table = {}

    def should_notify(self):
        if self.getact("tb.inst.clk") == 1:
            for key, tab in self.table.items():
                v = self.getval(key)
                tab[v] = 1 + (0 if v not in tab else tab[v])
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: fpconv.py <input-file.vcd>")
        exit(1)

    # test, so let's see everything
    logging.basicConfig()
    logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)

    # Create a parser object
    # parser = vcd.VCDParser(log_level=logging.DEBUG)
    parser = vcd.VCDParser(log_level=logging.INFO)

    watch = [
        "tb.inst.cnt",
        "tb.inst.r",
    ]

    # attach a watcher within the hierarchy and start running
    watcher = FPConvWatcher(parser, sensitive=["tb.inst.clk"], watch=watch, trackers=[])

    for key in watch:
        watcher.table[key] = {}

    with open(sys.argv[1]) as vcd_file:
        parser.parse(vcd_file)

    for key, tab in watcher.table.items():
        print(key)
        with (Path(__file__).parent / (key + ".csv")).open("w", newline="") as fptr:
            writer = csv.writer(fptr, delimiter="\t")
            writer.writerow(["value", "frequency"])
            for k, v in tab.items():
                if isinstance(k, str):
                    writer.writerow([k if k[0] != "b" else ("0%s" % k), v])
                else:
                    writer.writerow([k, v])
