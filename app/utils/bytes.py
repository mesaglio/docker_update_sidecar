def parse_bytes(bytes):
    bytes = bytes.decode("utf-8")
    if "\n" in bytes:
        bytes = bytes.split("\n")
    return bytes
