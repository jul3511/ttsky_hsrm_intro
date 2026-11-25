# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # uo_out[1:0] = ui_in[1:0] + uio_in[1:0] (2 Bit, Übertrag fällt weg)
    for a in range(4):
        for b in range(4):
            dut.ui_in.value = a
            dut.uio_in.value = b
            await ClockCycles(dut.clk, 1)
            assert dut.uo_out.value == (a + b) % 4
