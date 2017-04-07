#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import ftransc_gui.gui
from PyQt5 import QtWidgets


class FtranscGuiTestCase(unittest.TestCase):
    def test_window(self):
        window = ftransc_gui.gui.Window()
        self.assertTrue(isinstance(window, QtWidgets.QDialog))

        window_methods = [
            'convert',
            'browser',
            'add_files',
            'createFilesTable',
            'createButton',
            'delete_items',
        ]

        for method in window_methods:
            self.assertTrue(hasattr(window, method), 'Expected the Window instance to have the method: %s' % method)

    def test_app(self):
        app = ftransc_gui.gui.App([])
        self.assertTrue(isinstance(app, QtWidgets.QApplication))

if __name__ == '__main__':
    unittest.main()
