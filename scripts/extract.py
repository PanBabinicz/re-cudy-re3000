import os
import sys
import firmware_part as fwp

class extractor:
    def __init__(self):
        """ factory firmware
        self.firmware_parts=[
            fwp.firmware_part("begin",    0x00000000, 0x00036C60-0x00000000, 0),
            fwp.firmware_part("dtb0",     0x00036C60, 0x000CA9E9-0x00036C60, 0),
            fwp.firmware_part("dtb1",     0x000CA9E9, 0x000F0000-0x000CA9E9, 0),
            fwp.firmware_part("dtb2",     0x000F0000, 0x00430000-0x000F0000, 0),
            fwp.firmware_part("squashfs", 0x00430000, 0x00D20000-0x00430000, 0),
            fwp.firmware_part("jffs2",    0x00D20000, 0x01000050-0x00D20000, 0),
        ]
        """

        # 2.4.17-20250811-185007
        self.firmware_parts=[
            fwp.firmware_part("begin",    0x00000000, 0x0005A9F9-0x00000000, 0),
            fwp.firmware_part("dtb0",     0x0005A9F9, 0x00080800-0x0005A9F9, 0),
            fwp.firmware_part("dtb1",     0x00080800, 0x003C0800-0x00080800, 0),
            fwp.firmware_part("squashfs", 0x003C0800, 0x008A5000-0x003C0800, 0),
        ]
        self.op=None
        self.file=None
        self.argc=len(sys.argv)
        if (self.argc==1):
            print("Invalid use, check --help")
            sys.exit()
        elif (self.argc==2):
            self.op = sys.argv[1]
            if (self.op=="--help"):
                self.help()
                sys.exit()
            else:
                print("Invalid use, check --help")
                sys.exit()
        elif (self.argc==5):
            self.op=sys.argv[1]
            self.truncate=int(sys.argv[2])
            self.file=sys.argv[3]
            self.path=sys.argv[4]
        else:
            print("Invalid use, check --help")

    def get_real_size(self):
        for i in range(0, len(self.firmware_parts)):
            self.firmware_parts[i].real_size=os.path.getsize(self.path+'/'+self.firmware_parts[i].name)

    def start(self):
        self.get_real_size()
        for i in range(0, len(self.firmware_parts)):
            print(self.firmware_parts[i].total_size)
        if (self.op=="unpack"):
            file_in=open(self.file, 'rb')
            for part in self.firmware_parts:
                file_out=open(self.path+"/"+part.name, 'wb')
                file_in.seek(part.offset, 0)
                data=file_in.read(part.size)
                file_out.write(data)
                file_out.close()
            file_in.close()
        elif (self.op=="pack"):
            file_out=open(self.file, 'wb')
            for i in range(0, len(self.firmware_parts)-1):
                part_curr=self.firmware_parts[i]
                file_in=open(self.path+"/"+part_curr.name, 'rb')
                data=file_in.read(part_curr.real_size)
                file_out.write(data)
                padding=(part_curr.total_size-part_curr.real_size)
                file_out.write(b'\xff'*padding)
                print(f"Padding {part_curr.name} - {hex(padding)}")
                file_in.close()
            part_curr=self.firmware_parts[len(self.firmware_parts)-1]
            file_in=open(self.path+'/'+part_curr.name, 'rb')
            data=file_in.read(part_curr.real_size)
            file_out.write(data)
            file_in.close()
            padding=(self.truncate-(part_curr.offset+part_curr.real_size))
            print(f"Padding {part_curr.name} - {hex(padding)}")
            file_out.write(b'\xff'*padding)
            file_out.close()

    def help(self):
        print("Usage: python extract.py <operation: (pack/unpack)> <truncate-to-length> <bin-file> <exctraction-path>")

    def print_settings(self):
        print("Operation: "+self.op)
        print("File: "+self.file)

dev=extractor()
dev.start()
