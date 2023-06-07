# IBM_model_1
Based on statistics, the IBM_model_1 is used to evaluate and compare the quality of language alignment
data from WMT
link：https://pan.baidu.com/s/14SV1dU3cZ6o4Fjo-rxIBPQ 
code：73lc

1.open the file and download data
2.cmd：pip install spacy -i https://pypi.tuna.tsinghua.edu.cn/simple
       pip install en_core_web_sm-3.5.0.tar.gz
       pip install zh_core_web_sm-3.5.0.tar.gz




Selecting high-quality sentence pairs to form a training set to improve the performance of machine translation system has always been an important application of sentence pair quality evaluation. When the upper limit of model optimization is reached, you can consider reasonable optimization of the training set.

实验过程：
1.数据准备：

准备平行语料库，其中包含源语言和目标语言的句子对。
进行预处理，包括分词、去除标点符号等。

2.初始化模型参数：

定义源语言词汇表和目标语言词汇表，包括源语言词汇总数和目标语言词汇总数。
初始化翻译概率表，即源语言词汇到目标语言词汇的初始翻译概率。

3.Expectation-Maximization (EM) 算法迭代：

进行多轮迭代，直到模型收敛。
对于每个源语言句子和目标语言句子对：
Expectation 步骤：计算对齐概率（对齐期望），即源语言词汇和目标语言词汇的对齐概率。
Maximization 步骤：根据对齐概率更新翻译概率表。

4.对齐结果：

根据训练得到的翻译概率表，对新的源语言句子和目标语言句子对进行对齐。
