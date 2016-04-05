#! /usr/bin/python3
from configparser import ConfigParser
from os.path import exists, expanduser, dirname, join, isdir
from os import listdir
from collections import namedtuple
import pickle

QAPair = namedtuple('QAPair', ['question', 'answer'])


def load_qas(path):
    """ Load question answers pairs.

        Files starting with '.' are skipped.
        Does not work recursive on folders.

        Parameters
        ----------
        path : str
            Path to corpus file or folder containing corpus files.
            File(s) are pickled list(s) of QAPair objects.

        Returns
        -------
        quas : list of QAPair objects
    """

    path = expanduser(path)

    if isdir(path):
        filelist = [join(path, filename) for filename in listdir(path) if not filename.startswith('.')]
    else:
        filelist = [path]

    qas = [] # stands for questions and answers ...
    for filepath in filelist:

        with open(filepath, 'rb') as f:
            new_qas = pickle.load(f)

        qas.extend(new_qas)

    return qas


def load_configuration():

    CONFPATH = dirname(__file__) # configuration file is stored in source folder
    CONFNAME = 'memory_networks.cfg'

    default_config = {
    'QuestionAnswering' : {
        'corpus_path' : expanduser('~/mn_corpus/qa'),
        }
    }

    fullpath = join(CONFPATH, CONFNAME)
    conf = ConfigParser()
    conf.read_dict(default_config)
    if exists(fullpath):
        conf.read(fullpath)
    else:
        print('No configuration file found. Create new one in:', CONFPATH)
        with open(fullpath, 'w') as f:
            conf.write(f)

    return conf


def example():
    conf = load_configuration()
    corpus_path = conf['QuestionAnswering']['corpus_path']
    qas = load_qas(corpus_path)

    import random
    i = random.randint(0,len(qas)-1)
    print(qas[i].question)
    print(qas[i].answer)

    ...
