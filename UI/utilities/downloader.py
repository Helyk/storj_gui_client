# -*- coding: utf-8 -*-

import logging

import requests

from PyQt4 import QtCore


class DownloadTaskQtThread(QtCore.QThread):

    __logger = logging.getLogger('%s.DownloadTaskQtThread' % __name__)

    tick = QtCore.pyqtSignal(int, name="upload_changed")

    def __init__(self, url, path_to_save, options_chain, progress_bar):
        QtCore.QThread.__init__(self)
        self.obj_thread = QtCore.QThread()
        self.url = url
        self.path_to_save = path_to_save
        self.options_chain = options_chain
        self.progress_bar = progress_bar

        # def run(self):
        # self.client.create_download_connection(self, None, None, None, None)

    # def create_download_connection(self, url, path_to_save, options_chain, progress_bar):
    def run(self):
        self.__logger.debug('test run downloader')

        local_filename = self.path_to_save

        if self.options_chain['handle_progressbars'] != '1':
            r = requests.get(self.url)

            # requests.
            with open(self.local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        else:
            r = requests.get(self.url, stream=True)
            with open(local_filename, 'wb') as f:
                if self.options_chain['file_size_is_given'] == '1':
                    file_size = self.options_chain['shard_file_size']
                else:
                    file_size = int(r.headers['Content-Length'])

                chunk = 1
                num_bars = float(file_size) / chunk
                t1 = file_size / (32 * 1024)
                i = 0

                self.__logger.debug('file_size=%d', file_size)

                for chunk in r.iter_content(32 * 1024):
                    f.write(chunk)
                    self.__logger.debug('%s %s' % (str(i), str(t1)))
                    self.__logger.debug(round(float(i) / float(t1), 1))
                    self.__logger.debug('%s %' % str(int(round((100.0 * i) / t1))))
                    percent_downloaded = int(round((100.0 * i) / t1))

                    # Refactor for fix SIGSEGV
                    # self.tick.emit(percent_downloaded)
                    # self.emit(SIGNAL("setStatus"), percent_downloaded , "information")
                    # Old
                    # progress_bar.setValue (percent_downloaded)

                    i += 1
