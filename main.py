
import argparse
import v8unpack
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description="Unpack 1C EPF file to BSL using v8unpack")
    parser.add_argument("--epf", required=True, help="Path to the EPF file")
    parser.add_argument("--out", required=True, help="Output directory for BSL files")
    args = parser.parse_args()

    epf_path = os.path.abspath(args.epf)
    out_dir = os.path.abspath(args.out)

    if not os.path.exists(epf_path):
        raise FileNotFoundError(f"EPF file not found: {epf_path}")
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:
        v8unpack.extract(epf_path, out_dir)
        print(f"Successfully unpacked {epf_path} to {out_dir}")
    except Exception as e:
        raise Exception(f"Error unpacking EPF: {str(e)}")

    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith(".bsl"):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, out_dir)
                dst_path = os.path.join(out_dir, rel_path.replace(os.sep, "_"))
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.move(src_path, dst_path)

if __name__ == "__main__":
    main()