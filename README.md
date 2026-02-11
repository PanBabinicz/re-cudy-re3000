# Cudy RE3000 reverse engineering

## Introduction

> The Cudy RE3000 is a consumer-grade Wi-Fi 6 range extender designed to expand wireless
> coverage in residential and small-office environments. It supports dual-band operation,
> mesh functionality, and web-based configuration for managing wireless and network settings.
>
> This project focuses on reverse engineering the Cudy RE3000 with the primary objective of
> obtaining root-level privileges on both the factory-installed firmware and the latest officially
> released firmware. Root access enables full inspection of the device’s operating system,
> configuration mechanisms, and internal services.
>
> A key goal of this research is to analyze and modify wireless parameters beyond the limitations
> imposed by the stock firmware interface. This includes examining how regulatory domain settings,
> transmit power limits, channel configuration, and other radio parameters are implemented and
> enforced at the software level.
>
> By comparing the behavior and protections present in the factory firmware against those
> introduced in newer firmware versions, this project evaluates how the device’s security model
> evolves over time, particularly with respect to privilege escalation, configuration integrity,
> and firmware validation mechanisms.

> [!NOTE]
> **All activities described in this project are conducted for educational and security research purposes
> on owned hardware. The findings are intended to contribute to a better understanding of consumer
> networking device security and configuration integrity, and to promote transparency in embedded
> wireless system design.**

## UART Access and Initial Observations

> The Cudy RE3000 PCB exposes an accessible serial interface via clearly populated header pins. This
> significantly simplified early-stage hardware reconnaissance compared to devices where UART pads must
> be located manually.
>
> The device was powered using a laboratory power supply set to the nominal input voltage. Measurements
> taken after the power transformer stage indicated a supply voltage in the range of **12.4–12.5 V**, consistent
> with the device’s expected operating conditions.
>
> A USB-to-UART adapter was connected to the serial header using the following parameters:
>     - **Baud rate:** 115200
>     - **Logic level:** 3.3V
>     - **Interface:** TX, RX, GND
>
> Upon boot, the serial console produced verbose debug output, confirming that the interface operates as a
> standard 3.3V TTL UART. The boot log provided visibility into the bootloader stage, kernel initialization,
> and early userspace processes.
