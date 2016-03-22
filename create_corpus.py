"""self."""

import xml.etree.ElementTree as ET
from os.path import expanduser, join
from os import makedirs
import re
from main import load_configuration, QAPair, load_qas

def answers_wikia_iter():
    """
    Iteratates of question and answers pairs from answers.wiki.com 'Current pages dump'

    link: http://s3.amazonaws.com/wikia_xml_dumps/a/an/answers_pages_current.xml.7z
    link on site: http://answers.wikia.com/wiki/Special:Statistics
    """

    xml_filepath = expanduser('answers_pages_current.xml')
    tree = ET.parse(xml_filepath)
    pages = tree.getroot().findall('page')
    
    #start_cutout_phrases = ['User talk:', 'Forum:', 'File:', 'Talk:', 'User:','Category:','Template','MediaWiki:','Help:']
    #cutout_phrases = ['wikianswers']
    
    for p in pages:
        
        question = p.find('title').text
        answer = p.find('revision').find('text').text
        
        # skip if stats with sart-cutout-phrase
        #if any(title.startswith(scp) for scp in start_cutout_phrases):
        #    continue
        
        # skip if contains cutout-phrase
        #if any(title.lower().startswith(scp) for scp in cutout_phrases):
        #    continue

        # skip empty answers
        if not answer: continue

        # skip questions not marked as answered
        if '[Category:Answered questions]' not in answer:
            continue

        # cut certain bracket contents
        bracket_patterns = [
            r'\[\[.*\]\]',
            r'<.*>',
            r'\{\{.*\}\}',
        ]
        for pat in bracket_patterns:
            answer = re.sub(
                pattern = pat,
                repl = ' ',
                string = answer,
                flags = re.DOTALL)

        # remove uneccessary blanks
        answer = answer.strip()

        # if answer hsa been stripped empty, skip it!
        if not answer: continue

        yield QAPair(question, answer)


def save_to_pickle(filename, qas):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(qas, f)


if __name__ == '__main__':
    import sys; args = sys.argv[1:]
    conf = load_configuration()

    if 'load' in args:
        qas = load_qas(conf['QuestionAnswering']['corpus_path'])
    else:
        print('read xml file ...')
        qas = list(answers_wikia_iter())

    if 'save' in args:
        print('pickle ...')
        conf = load_configuration()
        corpus_path = conf['QuestionAnswering']['corpus_path']
        makedirs(corpus_path, exist_ok=True)
        filepath = join(corpus_path, 'answers.wikia.p')
        save_to_pickle(filepath, qas)

    if 'loop' in args:
        print('loop over qa_pairs\n')
        from random import shuffle; shuffle(qas)
        for q,a in qas:
            print('Q:', q)
            print('A:', a, '\n')
            input()
