#!/usr/bin/env sh

set -e

cd $(dirname "$0")

echo "> Analyze tb.vhd"
ghdl -a --std=08 ent.vhd tb.vhd

echo "> Elaborate tb"
ghdl -e --std=08 tb

echo " > Run tb"
ghdl -r --std=08 tb --stop-time=1us --vcd=wave.vcd

rm *.cf
