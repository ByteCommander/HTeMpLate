#!/usr/bin/env python3
import os
import re
import sys
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 {} <BASEPATH> <SOURCE_SUBDIRECTORY> <DESTINATION_SUBDIRECTORY>".format(sys.argv[0]))
        print()
        print("Set <BASEPATH> to be yor project root folder.")
        print("<SOURCE_SUBDIRECTORY> will be the folder to watch, which contains your sources, normally 'src'.")
        print("<DESTINATION_SUBDIRECTORY> will be the folder to which HTeMpLate will write the built files.")
        print("Note that before every build it will delete all content of this directory!")
        print("Both <SOURCE_SUBDIRECTORY> and <DESTINATION_SUBDIRECTORY> must be relative to <BASEPATH>.")
        exit(1)

    path, src_suffix, dest_suffix = [s.strip().strip("\"").strip('') for s in sys.argv[1:]]

    run(path, src_suffix, dest_suffix)


def run(path, src_suffix, dest_suffix):
    srcpath = os.path.join(path, src_suffix)
    destpath = os.path.join(path, dest_suffix)

    print("WARNING! All files in the destination directory")
    print("    " + destpath)
    print("will be DELETED before every automatic rebuild.")
    print()
    yn = input("Are you sure you want to proceed? (y/N) ")
    if yn.lower() != "y":
        print("Aborted.")
        exit(2)

    observer = Observer()
    handler = MyEventHandler(srcpath, destpath)
    observer.schedule(handler, srcpath, True)

    print()
    print("Starting automatic file system watcher on {}".format(srcpath))

    handler.dispatch(DirCreatedEvent(path))
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        observer.stop()
    observer.join()


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, srcpath, destpath):
        self.srcpath = srcpath
        self.destpath = destpath

    def on_any_event(self, event):
        print()
        print("File system event ({}) detected on {}".format(event.event_type, event.src_path))
        build_website(self.srcpath, self.destpath)
        print("Finished building.")


def build_website(srcpath, destpath):
    shutil.rmtree(destpath)
    for (dirpath, dirnames, filenames) in os.walk(srcpath):
        if ".htempignore" not in filenames:
            for filename in filenames:
                inputfile = os.path.join(dirpath, filename)
                outputfile = os.path.join(destpath, os.path.relpath(inputfile, srcpath))

                if not os.path.exists(os.path.dirname(outputfile)):
                    os.makedirs(os.path.dirname(outputfile))

                try:
                    if inputfile.endswith(".html"):
                        print("* Building HTML " + inputfile + " -> " + outputfile)
                        build_html(inputfile, outputfile)
                    else:
                        print("* Cloning " + inputfile + " -> " + outputfile)
                        shutil.copy(inputfile, outputfile)
                except Exception as e:
                    print(e)
        else:
            print("* Ignoring directory {} because of .htempignore file.".format(dirpath))


def build_html(inputfile, outputfile):
    with open(inputfile) as input_f, open(outputfile, mode="w") as output_f:
        def replacer(match):
            indent, file = match.groups()
            print("  > Including " + file)
            with open(os.path.join(os.path.dirname(inputfile), file)) as f:
                return "".join(indent + line for line in f).lstrip("\n").rstrip()

        result = re.sub(r"([ \t]*)<!--\s*INCLUDE\s*\(\s*(.*)\s*\)\s*-->[ \t]*", replacer, input_f.read())
        output_f.write(result)


if __name__ == "__main__":
    main()
