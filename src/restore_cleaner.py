"""Cleans the restore directory so old checkpoints don't clog it up.
"""

import os.path
import time


def main():
    """Runs the cleaner loop.

    """
    while True:

        # pylint: disable=invalid-name
        files = sorted(os.listdir("../restores"))

        if len(files) > 5:
            # pylint: disable=invalid-name
            number_restore = []
            for file in files:
                number_restore.append(int(file[16:]))

            sorted_restore = sorted(number_restore)

            print("Removing file: neat-checkpoint-" + str(sorted_restore[0]))
            os.remove(os.path.join("../restores", "neat-checkpoint-" + str(sorted_restore[0])))

        time.sleep(300)


if __name__ == '__main__':
    main()
