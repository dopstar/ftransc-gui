import os
import sys
import logging

import ftransc.utils
import ftransc_gui.gui


def gui():
    opt, files = ftransc.utils.parse_args()

    if opt.silent:
        log_level = logging.CRITICAL
    elif opt.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    log_format = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
    logging.basicConfig(stream=sys.stdout, level=log_level, format=log_format)

    if os.environ['USER'] == 'root':
        raise SystemExit('It is not safe to run ftransc as root.')

    app = ftransc_gui.gui.App(sys.argv)
    ftransc_gui.gui.Window().show()
    sys.exit(app.exec_())
