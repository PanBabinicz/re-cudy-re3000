class firmware_part:
    def __init__(self, name, offset, total_size, real_size):
        self.name = name
        self.offset = offset
        self.total_size = total_size
        self.real_size = real_size
