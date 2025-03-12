print("hello world")

from textnode import TextNode
from gencontent import generate_pages_recursive
import os, shutil
import sys

def clean_directory(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
        return
    
    shutil.rmtree(dir)

    os.mkdir(dir)


def rec_copy(from_dir, to_dir):
    if not os.path.exists(from_dir):
        raise RuntimeError("Directory to be copied from doesn't exist")
    if not os.path.exists(to_dir):
        raise RuntimeError("Directory to be copied to doesn't exist")
    
    for f in os.listdir(from_dir):
        p = os.path.join(from_dir, f)
        if os.path.isfile(p):
            print(f"Copy {f} from {p} to {to_dir}")
            shutil.copy(p, to_dir)
        elif os.path.isdir(p):
            d = os.path.join(to_dir, f)
            old_d = os.path.join(from_dir, f)
            print(f"Making dir {d}")
            os.mkdir(d)
            print(f"Calling rec_copy from {old_d} to {d}")
            rec_copy(old_d, d)
        else:
            raise RuntimeError(f"{p} is neither a file nor a directory?")
        


def main():

    # n = TextNode("Abcd", "", "http://tarnow.pl")

    # print(n)

    basepath = "/"
    if len(sys.argv) > 1 and isinstance(sys.argv[1], str):
        basepath = sys.argv[1]

    clean_directory("./docs")
    rec_copy("./static", "./docs")

    print(basepath)

    # print("Generating page ->")
    # generate_page(
    #     os.path.join("./content", "index.md"),
    #     "./template.html",
    #     os.path.join("./public", "index.html")
    # )

    print("Generating content...")
    # generate_pages_recursive("./content", "./template.html", "./public")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
    main()
