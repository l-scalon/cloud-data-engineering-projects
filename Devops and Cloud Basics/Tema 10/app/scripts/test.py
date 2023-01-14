import main, cleanup, absolute, unittest, sys
from os import path, walk

# @@@@@ ///// WARNING \\\\\ @@@@@
# This script should be used for development purposes only.
# Make a copy of the /tweets/ folder before running this script or the files will be lost.
# @@@@@ \\\\\ WARNING ///// @@@@@

class FileTest(unittest.TestCase):
    def test_if_file_was_created(self):
        tweets_folder = path.join(absolute.path(), 'tweets')
        total_files = 0
        total_folders = 0
        for base, folders, files in walk(tweets_folder):
            for Folders in folders:
                total_files += 1
            for Files in files:
                total_folders += 1
        self.assertEqual(1, total_files)
        self.assertEqual(1, total_folders)

def test():
    try: 
        cleanup.cleanup()
        main.main()
        unittest.main()
    finally:
        cleanup.cleanup()

if __name__ == "__main__":
    test()