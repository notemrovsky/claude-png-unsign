import struct
import argparse


def strip_c2pa(input_path, output_path):
    with open(input_path, "rb") as f:
        sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            print("not a valid png file")
            return

        chunks = []
        stripped = False
        while header := f.read(8):
            length, type = struct.unpack(">I4s", header)
            data = f.read(length)
            crc = f.read(4)
            if type.decode() == "caBX":
                stripped = True
                continue
            chunks.append(header + data + crc)

    if not stripped:
        print("no c2pa chunk found, file is already clean")
        return

    with open(output_path, "wb") as f:
        f.write(sig)
        for c in chunks:
            f.write(c)

    print(f"done, saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="input png file")
    parser.add_argument("-o", required=True, help="output png file")
    args = parser.parse_args()
    strip_c2pa(args.i, args.o)
