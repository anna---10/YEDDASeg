YEDDASeg: Textual Topic Segmentation Annotation tool
======

About:
====
YEDDASeg is developed for manually annotating segments of topics in textual information. It can be used for any language, considering all styles of text. Differently from entity annotation, the topic segmentation concerns in finding chunks/sequential blocks of texts that are semantically close in the text. Therefore, the interface for this kind of annotation is facilitated by simply placing the cursor in a position in the text and pressing a key that represent the segment's title in the next lines. It is compatiable with all mainstream operating systems includings Windows, Linux and MacOS. This GUI annotation tool is developed with tkinter package in Python. 

YEDDASeg is based on [YEDDA Project](https://github.com/jiesutd/SUTDAnnotator) SUTDAnnotator, useful mostly for NER, developed by *Jie Yang*. More details can be seen in the [author's paper](https://arxiv.org/pdf/1711.03759.pdf). YEDDASeg is maintained by the Apache License.

System required: Python 2.7

Author: *Thiago de Sousa Silveira*, master student at Tsinghua University.

Interface:
====
It provides both annotator interface for efficient annotatation:
* Annotator Interface:
 ![alt text](https://github.com/ThiagoSousa/YEEDASeg/blob/master/annotatorinterface.png "Interface demo")

Use as an annotator ?
====
* Configure your segment labels in the `config` file. 
 ![alt text](https://github.com/ThiagoSousa/YEEDASeg/blob/master/config.png "Config file example")
* Start the interface: run `python YEDDA_Annotator.py`
* Click `Load Next File` button and select your input file.
* Click `Save` button to save your annotations, or simply load the next file, it already saves. It will save a `.ann` with the annotated tags in the same directory you have. 

To Annotate: 
* Place the cursor in a position in the text and press the key that represent the segment that comes next to that position. 
* For example, in the following news article, the annotator wants to tag the title segment, so the annotator, place the cursor in the beginning of the file and press `0` for the `title` tag. The title tag is placed in the file. The tag is saved in the format `<<<tag>>>`
![alt text](https://github.com/ThiagoSousa/YEEDASeg/blob/master/example1.png "Example 1")
![alt text](https://github.com/ThiagoSousa/YEEDASeg/blob/master/example2.png "Example 2")
* To remove a tag, just put the cursor within a tag and press `q`. 
* Also, if you want to edit it, place the cursor within a tag and press the key you want to change it to.

* A list of demo text can be seen in the folder `demotext`. They are annotated with news tags' segments, such as title, introduction, quote, citation, facts, endings.

Cite:
=====
If you use this tool or modify this tool, I recommend citing the original [YEDDA's](https://arxiv.org/pdf/1711.03759.pdf) report:

	@article{yang2017yedda,  
	 title={YEDDA: A Lightweight Collaborative Text Span Annotation Tool},  
	 author={Jie Yang and Yue Zhang},  
	 Journal = {arXiv preprint arXiv:1711.03759},
	 year={2017}  
	}

Updates:
====
* 2018-Apr-20, (V 0.1): init version.
* 2018-Apr-19, Forked from YEDDA SUTDAnnotator.

