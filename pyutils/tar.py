import argparse
import sys
import os
import tarfile


def ignore_dirs(exclude_dirs, d):
    for x in exclude_dirs:
        if d.endswith(x):
            return True

    return False


def ignore_files(exclude_files, exclude_dirs,f):
    for x in exclude_files:
        if x.startswith('*'):
            x = x[1:]
        if f.endswith(x):
            return True

    par = os.path.split(f)[0]
    for x in exclude_dirs:
        if x in f:
            return True
    return False


def collectfiles(source, exclude_files, exclude_dirs):
    flist = set()
    for root, dir, files in os.walk(source):
        #print("root:{} dir:{} total:{}".format(root, dir, len(files)))
        root=root[len(source):]
        root = "."+root

        if ignore_dirs(exclude_dirs, root):
            print("    ignore:%s" % root)
            continue

        for f in files:
            f = os.path.join(root,f)
            if ignore_files(exclude_files,exclude_dirs, f):
                print ("    ignore:%s" % f)
                continue

            flist.add(f)
            print("add:%s" % f)

    return flist


def tarfiles(source, flist):
    par = os.path.split(source)[0]
    os.chdir(source)
    bakfile = os.path.join(par, source + "_bak.tar.gz")

    t = tarfile.open(bakfile, "w:gz")
    for f in flist:
        t.add(f)
    t.close()
    print ("tarfiles:%s" % bakfile)


def main():
    if len(sys.argv) < 2:
        print("usage: python tar.py <directory>")
        return

    # directory = sys.argv[1]
    # print("directory:%s"%directory)

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="source directory")

    parser.add_argument("-e", "--exclude", help="ignore some files")

    parser.add_argument("-e2", "--exclude2", help="ignore some directories")
    args = parser.parse_args()
    if not args.source:
        print("source directory is nil")
        return
    source = args.source
    if source[-1] == os.path.sep:
        source = source[:-1]

    print("source directory is %s" % source)

    exclude_files = [".DS_Store",".gitignore"]
    if args.exclude:
        s = args.exclude
        print("ignore some files:%s" % s)
        exclude_files += s.split(":")
    for i in exclude_files:
        print(i)

    exclude_dirs = [".git",".idea"]
    if args.exclude2:
        s = args.exclude2
        print("ignore some directories:%s" % s)
        exclude_dirs += s.split(":")
    for i in exclude_dirs:
        print(i)

    flist = collectfiles(source, exclude_files, exclude_dirs)
    if not flist:
        print("tar nothing")
        return

    tarfiles(source, flist)

    pass


if __name__ == '__main__':
    main()
