"""
Does She Wink or Does She Nod? A Challenging Benchmark for Evaluating Word Understanding of Language Models
https://www.aclweb.org/anthology/2021.eacl-main.42/

@inproceedings{senel-schutze-2021-wink,
    title = "Does She Wink or Does She Nod? A Challenging Benchmark for Evaluating Word Understanding of Language Models",
    author = {Senel, Lutfi Kerem  and
      Sch{\"u}tze, Hinrich},
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume",
    month = apr,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.eacl-main.42",
    pages = "532--538",
    abstract = "Recent progress in pretraining language models on large corpora has resulted in significant performance gains on many NLP tasks. These large models acquire linguistic knowledge during pretraining, which helps to improve performance on downstream tasks via fine-tuning. To assess what kind of knowledge is acquired, language models are commonly probed by querying them with {`}fill in the blank{'} style cloze questions. Existing probing datasets mainly focus on knowledge about relations between words and entities. We introduce WDLMPro (Word Definitions Language Model Probing) to evaluate word understanding directly using dictionary definitions of words. In our experiments, three popular pretrained language models struggle to match words and their definitions. This indicates that they understand many words poorly and that our new probing task is a difficult challenge that could help guide research on LMs in the future.",
}
"""


import json
import os
from lm_eval.base import Task
from ..utils import sh


class D2W(Task):
    VERSION = 0

    def __init__(self):
        super().__init__()

    def download(self):
        if not os.path.exists('data/quac'):
            sh("""
                wget https://www.cis.lmu.de/definition benchmark/WDLAMPro.zip
                unzip WDLAMPro.zip
                """)

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return False

    def training_docs(self):
        myjson = json.load(open('data/WDLAMPro/WDNLAMPro.json'))
        return self.load_doc(myjson)

    def validation_docs(self):
        raise NotImplementedError("WDLAMPro has no test docs.")

    def test_docs(self):
        raise NotImplementedError("WDLAMPro has no test docs.")
    
    def fewshot_description(self):
        # TODO: figure out fewshot description
        desc = "Given the definition of a word and a set of options, choose an option which matches the definition given.\nFor example, 'To breathe easily again, as after exertion or anxiety is the definition of' \nOptions: 'respire', 'choke', 'exhale', 'hiccup', 'hyperventilate', 'inhale', 'sigh', 'snore', 'wheeze', 'yawn', \nAnswer: respire"
        return desc

    def load_doc(self, myjson):
        examples = []
        for sample_no, (target_syn, candidates) in enumerate(WDLAMPro["v"].items())::
            target_definition = candidates[target_syn]
            target_word = target_syn.split('.')[0].replace("_", " ")
            options = [word.split('.')[0].replace("_", " ") for word in candidates.keys()]
            defin = f'To {target_definition} is the definition of'
            example = {'prompt': defin, 'options': options, 'answer': target_word}
            examples.append(example)
            
        for sample_no, (target_syn, candidates) in enumerate(WDLAMPro["n"].items())::
            target_definition = candidates[target_syn]
            target_word = target_syn.split('.')[0].replace("_", " ")
            options = [word.split('.')[0].replace("_", " ") for word in candidates.keys()]
            defin = f'{target_definition} is the definition of'
            
            example = {'prompt': defin, 'options': options, 'answer': target_word}
            examples.append(example)
        
        return examples
    
    def doc_to_text(self, doc):
        return doc['prompt'] + '\n' + 'options: ' + doc['options'] + '\n\n' + 'A: '

    def doc_to_target(self, doc):
        return doc['answer']

    def construct_requests(self, doc, ctx):
        """ Uses RequestFactory to construct Requests and returns an iterable of 
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural 
            language description, as well as the few shot examples, and the question
            part of the document for `doc`. 
        """
        ll, is_prediction = rf.loglikelihood(ctx, doc['answer'])
        return is_prediction
    
    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a 
        dict where keys are the names of submetrics and values are the values of 
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        is_prediction, = results
        return {
            "acc": is_prediction
        }
        

        
