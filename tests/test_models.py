import pytest
import lm_eval.models as models


def test_gpt2():
    gpt2 = models.get_model('gpt2').create_from_arg_string("device=cpu")
    (ll_dog, ig_dog), (ll_cat, ig_cat), *vals = gpt2.loglikelihood([
        ('The quick brown fox jumps over the lazy', ' dog'),
        ('The quick brown fox jumps over the lazy', ' cat'),
        
        ("""A mult""", """ilayer perceptron (MLP) is a class of feedforward artificial neural network (ANN)"""), 
        ("""The term MLP is used ambiguously, sometimes loosely to any feedforward ANN, sometimes strictly to refer to networks composed of multiple layers of perceptrons""", """ (with threshold activation); see § Terminology"""), 
        ("""Multilayer perceptrons are sometimes coll""", """oquially referred to as "vanilla" neural networks, especially when they have a single hidden layer.[1]"""), 
        ("""An MLP consists of at least three layers of nodes: an input layer, a hidden layer and an output layer. Except for the input nodes, each node is a neuron that uses a nonlinear""", """ activation function."""), 
        ("""MLP utilizes a supervised""", """ learning technique called backpropagation for training.[2][3] Its multiple layers and non-linear activation distinguish MLP from a linear perceptron. It can distinguish data that is not linearly separable.[4]"""), 
        ("""Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic""", """ in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something which current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches. """), 
        ("""Specifically, we train GPT-3, an autoregressive language model with 175""", """ billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or fine-tuning, with tasks and few-shot demonstrations specified purely via text interaction with the model. GPT-3 achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly reasoning or domain adaptation, such as unscrambling words, using a novel word in a sentence, or performing 3-digit arithmetic. At the same time, we also identify some datasets where GPT-3's few-shot learning still struggles, as well as some datasets where GPT-3 faces methodological issues related to training on large web corpora. Finally, we find that GPT-3 can generate samples of news articles which human evaluators have difficulty distinguishing from articles written by humans. We discuss broader societal impacts of this finding and of GPT-3 in general."""), 
        ("""A mult""", """ilayer perceptron (MLP) is a class of feedforward artificial neural network (ANN)"""), 
        ("""Hello""", """ World"""), 
    ])

    assert ll_dog > ll_cat
    assert not ig_cat

    # test empty context
    gpt2.loglikelihood([('', 'test')])

    gen, = gpt2.greedy_until([
        ('The quick brown fox jumps over the lazy', ['.', '\n'])
    ])

    assert gen == ', lazy fox and they both fall to the ground'

    targets = [-61.60536193847656, -56.57843780517578, -62.131004333496094, -9.799489974975586, -153.96334838867188, -341.222900390625, -731.1475830078125, -61.60536193847656, -8.682319641113281]

    for (pred, _), tgt in zip(vals, targets):
        assert pred == pytest.approx(tgt)