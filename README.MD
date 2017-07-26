# HTeMpLate

> Simple dynamic template engine for HTML documents

Include external HTML snippets by simply writing a `<!-- INCLUDE(path/to/snippet.html) -->` comment inside the target document in the right place. The file system watcher will automatically rebuild all your documents every time you modify the sources. 

#### CLI Usage:

Run the script from a terminal with a Python 3 interpreter:

    python3 htemplate.py <BASEPATH> <SOURCE_SUBDIRECTORY> <DESTINATION_SUBDIRECTORY>

- Set `<BASEPATH>` to be yor project root folder.  
- `<SOURCE_SUBDIRECTORY>` will be the folder to watch, which contains your sources, normally something like `src`.
- `<DESTINATION_SUBDIRECTORY>` will be the folder to which HTeMpLate will write the built files, normally something like `dest`.

  Note that before every build it will *delete all content of this directory!*
  
Both `<SOURCE_SUBDIRECTORY>` and `<DESTINATION_SUBDIRECTORY>` must be relative to `<BASEPATH>`.")

#### Author and license:

This script was created by [ByteCommander](https://github.com/ByteCommander) and is available for free usage under the terms of the [MIT License](https://opensource.org/licenses/MIT), of which you can find a copy in the LICENSE.TXT.
