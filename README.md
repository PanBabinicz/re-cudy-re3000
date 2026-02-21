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
![SERIAL-LOGS](https://github.com/PanBabinicz/re-cudy-re3000/blob/master/screenshots/serial-logs.jpg)

## External Flash Removal and Firmware Extraction

> After confirming that the UART interface did not provide interactive access, attention shifted to the external
> SPI flash memory identified during the initial PCB inspection. Since the flash chip usually stores the bootloader,
> kernel, and root filesystem, extracting its contents would allow full offline analysis of the firmware.
>
> The SPI flash chip was carefully desoldered from the PCB to enable direct access. Proper hot-air rework
> techniques were used to minimize thermal stress and avoid damaging pads or surrounding components.
> Once removed, the chip was placed in a suitable adapter compatible with the XGecu T48 universal programmer.
>
> After obtaining the firmware image, `binwalk` was used to analyze its internal structure and identify embedded
> components. The scan revealed multiple structured regions, including device tree blobs and filesystem partitions.
>
> The relevant findings are shown below:

```console
-----------------------------------------------------------------------------------------------------------------------
DECIMAL                            HEXADECIMAL                        DESCRIPTION
-----------------------------------------------------------------------------------------------------------------------
224352                             0x36C60                            Device tree blob (DTB), version: 17, CPU ID: 0,
                                                                      total size: 586 bytes
829929                             0xCA9E9                            Device tree blob (DTB), version: 17, CPU ID: 0,
                                                                      total size: 7232 bytes
983040                             0xF0000                            Device tree blob (DTB), version: 17, CPU ID: 0,
                                                                      total size: 3386771 bytes
4390912                            0x430000                           SquashFS file system, little endian, version:
                                                                      4.0, compression: xz, inode count: 2068, block
                                                                      size: 262144, image size: 9319386 bytes,
                                                                      created: 2025-02-11 03:20:32
13762560                           0xD20000                           JFFS2 filesystem, little endian, nodes: 3282,
                                                                      total size: 2949132 bytes
-----------------------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 32.0 milliseconds
```
> The file system structure:

```console
[km1t4h@nobody squashfs-root]$ ls -al
total 68
drwxr-xr-x 16 km1t4h km1t4h 4096 Feb 11  2025 .
drwxr-xr-x  3 km1t4h km1t4h 4096 Feb 15 13:46 ..
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 bin
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 dev
drwxr-xr-x 26 km1t4h km1t4h 4096 Feb 11  2025 etc
-rwxr-xr-x  1 km1t4h km1t4h  276 Feb 11  2025 init
drwxr-xr-x 11 km1t4h km1t4h 4096 Feb 11  2025 lib
lrwxrwxrwx  1 km1t4h km1t4h    3 Feb 11  2025 lib64 -> lib
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 mnt
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 overlay
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 proc
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 rom
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 root
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 sbin
drwxr-xr-x  2 km1t4h km1t4h 4096 Feb 11  2025 sys
drwxrwxrwt  2 km1t4h km1t4h 4096 Feb 11  2025 tmp
drwxr-xr-x  7 km1t4h km1t4h 4096 Feb 11  2025 usr
lrwxrwxrwx  1 km1t4h km1t4h    3 Feb 11  2025 var -> tmp
drwxr-xr-x  4 km1t4h km1t4h 4096 Feb 11  2025 www
```

## Root Filesystem Modification and Size Constraints

> After extracting and analyzing the firmware image, attention shifted to modifying the root filesystem to
> introduce custom startup behavior. Inspection of the unpacked image revealed a standard embedded Linux layout
> with initialization scripts handled through the `rc.common` framework.
>
> To introduce persistent behavior at boot time, the relevant initialization logic was modified within the
> filesystem. The goal was to execute a custom networking command during system startup, allowing remote shell
> access once the device completed boot.
>
> However, rebuilding the SquashFS image introduced a critical limitation: the firmware partition allocated for
> the root filesystem had a strict maximum size of **9,371,648 bytes**. The unmodified SquashFS image already
> occupied the entire allocated space. Any changes—even minor ones—resulted in a filesystem image that exceeded
> this size constraint, causing the firmware to fail during boot.
>
> To resolve this constraint, non-essential files within the filesystem were identified and removed. In this case
>  certain font files were deleted to free sufficient space while preserving core system functionality. This
> allowed the rebuilt SquashFS image to remain below the maximum size limit.
>
> After ensuring the modified filesystem remained under the partition size limit, the image was padded to match
> the original expected firmware size.

## Startup Script Injection Attempts

> After successfully rebuilding and flashing the modified firmware, the next objective was to ensure that the
> custom logic executed reliably during system startup.
>
> The initial approach was to create a standalone `backdoor.sh` script and trigger it during boot. However,
> this method did not produce the expected behavior. The script did not execute.
>
> To improve reliability, the backdoor logic was embedded directly into existing initialization mechanisms.
> First, it was inserted into an `rc.common`-based startup script, as this framework is commonly used in embedded
> Linux systems (particularly OpenWrt-derived environments) to manage services. Despite correct syntax and
> integration, the logic still failed to execute as intended.
>
> As an additional attempt, the logic was placed into the system-wide `profile` file to trigger execution upon
> shell initialization. This also proved ineffective.
>
> To better understand the execution flow, the serial debug logs were closely analyzed during boot. This
> investigation revealed that a script named `firewall.include` was executed in certain condition as part of
> the networking and firewall initialization stage. This script appeared to be a promising candidate for reliable
> code execution. The next step was therefore to embed the backdoor logic within `firewall.include` and observe
> whether it executed consistently during boot.
