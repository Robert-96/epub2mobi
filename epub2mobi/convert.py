import sys
import pathlib
import subprocess

from loguru import logger


def is_epub(path):
    return pathlib.Path(path).suffix == ".epub"


def is_mobi(path):
    return pathlib.Path(path).suffix == ".mobi"


class EbookConverter:
    """Run the ebook-convert command and return the output.

    Args:
        inputpath (:obj:`str`): The input path.
        outputpath (:obj:`str`, optional): The output path.
        timeout (:obj:`int`, optional): The timeout in seconds.

    """

    def __init__(self, inputpath, outputpath=None, timeout=None):
        self.inputpath  = pathlib.Path(inputpath)
        self.outputpath =  pathlib.Path(outputpath) if outputpath else self.inputpath.with_suffix('.mobi')
        self.timeout = timeout

        if not self.inputpath.exists():
            raise FileNotFoundError('Path: {} doesn\'t exists.'.format(self.inputpath))
        if self.inputpath.suffix != '.epub':
            raise ValueError('Expecting an epub file; Got: {}'.format(self.inputpath))

        if self.outputpath.exists():
            raise FileExistsError('Path: {} already exists.'.format(self.outputpath))
        if self.outputpath.suffix != '.mobi':
            raise ValueError('Expecting an mobi file; Got: {}'.format(self.outputpath))

    @property
    def _path(self):
        if sys.platform == 'darwin':
            return '/Applications/calibre.app/Contents/MacOS/ebook-convert'
        else:
            return 'ebook-convert'

    def run(self):
        try:
            proc = subprocess.Popen(
                [self._path, str(self.inputpath), str(self.outputpath)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            outs, errs = proc.communicate(timeout=self.timeout)
        except TimeoutError:
            logger.exception('ebook-convert raised an timeout error.')
            proc.kill()

            outs, errs = proc.communicate()
            outs = outs.decode('utf-8')
            errs = errs.decode('utf-8')

            logger.debug('Output: {}', outs)
            logger.debug('Errors: {}', errs)

            raise TimeoutError(errs)

        outs = outs.decode('utf-8')
        errs = errs.decode('utf-8')

        logger.debug('Exit code: {}', proc.returncode)
        logger.debug('Output: {}', outs)
        logger.debug('Errors: {}', errs)

        if proc.returncode != 0 and not errs.startswith('ebook-convert raise the following warning'):
            raise Exception('ebook-convert raised the following error: {}'.format(errs))

        if errs:
            raise Warning('ebook-convert raise the following warning: {}'.format(errs))

        return outs, errs

    @classmethod
    def convert(cls, *args, **kwargs):
        converter = cls(*args, **kwargs)
        return converter.run()


def epub2mobi(inputpath, outputpath=None, timeout=None):
    """Convert an e-book from epub to mobi."""

    return EbookConverter.convert(inputpath, outputpath=outputpath, timeout=timeout)
