import codecs
import ftransc_gui
import ftransc_gui.constants


def get_display_version():
    major, minor, bugfix = ftransc_gui.__version__.split('.')
    release_code_name = ftransc_gui.constants.releases.get(minor, codecs.encode('dopstar', 'rot13'))
    if not bugfix.isdigit():
        return ftransc_gui.__version__
    return ''.join(
        [':' for _ in range(int(major))] + [release_code_name] + [':' for _ in range(int(bugfix))]
    )
