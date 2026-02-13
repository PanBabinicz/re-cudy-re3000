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

## Hardware Reconnaissance and PCB Inspection

> Before obtaining serial output from the device, the enclosure was carefully disassembled to allow inspection
> of the printed circuit board (PCB). The primary objective at this stage was to identify potential debugging
> interfaces and non-volatile storage components that could be useful for further analysis.
>
> The inspection focused on two key elements:

- **Serial port header (UART interface)**
- **External flash memory chip**

> Clearly exposed header pins consistent with a UART interface were identified on the PCB. Their placement and
> layout suggested a factory debugging interface, making them a natural starting point for low-level access.
>
> An external SPI flash memory chip was also located on the board. This component is typically used to store the
> bootloader, kernel, root filesystem, and configuration data. Identifying this chip early was important, as it
> represents a direct method of obtaining a full firmware dump if needed.
>
> The RF shielding covers protecting the main SoC and radio components were intentionally left in place during
> this stage. Although removing them would have revealed exact MCU and RF chipset markings, the initial focus was
> on accessible components relevant to firmware extraction and debugging rather than full hardware teardown.
>
> This hardware reconnaissance phase provided two critical entry points for further work:

1. **The UART interface for observing boot behavior.**
2. **The external SPI flash for potential firmware extraction and analysis.**

> With these targets identified, the next step was to establish a serial connection and observe the device’s boot
> process.

![INTERNAL-1](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/internal-1.jpg)
![FLASH](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/flash.jpg)
![SERIAL](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/serial.jpg)

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

- **Baud rate:** 115200
- **Logic level:** 3.3V
- **Interface:** TX, RX, GND

> Upon boot, the serial console produced verbose debug output, confirming that the interface operates as a
> standard 3.3V TTL UART. The boot log provided visibility into the bootloader stage, kernel initialization,
> and early userspace processes.

![POWER-CONNECTION](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/power-connection.jpg)
![UART-CONNECTION-1](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/uart-connection-1.jpg)
![POWER-SUPPLY](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/power-supply.jpg)
