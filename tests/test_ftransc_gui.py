#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import ftransc_gui.gui
from PyQt5 import QtWidgets


class FtranscGuiTestCase(unittest.TestCase):
    def test_window(self):
        self.assertTrue(issubclass(ftransc_gui.gui.Window, QtWidgets.QDialog))

        window_methods = [
            'convert',
            'browser',
            'add_files',
            'createFilesTable',
            'createButton',
            'delete_items',
        ]

        for method in window_methods:
            self.assertTrue(
                hasattr(ftransc_gui.gui.Window, method),
                'Expected the Window instance to have the method: %s' % method
            )

    def test_app(self):
        self.assertTrue(issubclass(ftransc_gui.gui.App, QtWidgets.QApplication))

if __name__ == '__main__':
    unittest.main()
