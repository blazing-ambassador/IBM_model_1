import spacy
# coding=utf-8
def load_data(file_path):
    """
    加载平行数据，每行包含一对汉英句子，以制表符分隔。
    返回两个列表，分别包含汉语句子和英语句子。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()

    chinese_sentences = []
    english_sentences = []

    for line in data:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            chinese, english = parts
            chinese_sentences.append(chinese)
            english_sentences.append(english)
    return chinese_sentences, english_sentences

def initialize_probabilities(chinese_sentences, english_sentences):
    """
    初始化翻译概率为均匀分布的字典。
    返回一个字典，其中键是英语词语，值是一个包含所有汉语词语的字典。
    """
    probabilities = {}
    ch_tokenizer = spacy.load("zh_core_web_sm")
    en_tokenizer = spacy.load("en_core_web_sm")
    for i in range(0, len(chinese_sentences)):
        chinese_sentences[i] = [w for w in ch_tokenizer(chinese_sentences[i])]

    for i in range(0, len(english_sentences)):
        english_sentences[i] = [w for w in en_tokenizer(english_sentences[i])]

    for english_sentence in english_sentences:
        for english_word in english_sentence:
            if english_word not in probabilities:
                probabilities[english_word] = {}
                for chinese_sentence in chinese_sentences:
                    for chinese_word in chinese_sentence:
                        probabilities[english_word][chinese_word] = 1.0 / len(chinese_sentence)

    # print(probabilities)
    return probabilities

def expectation_maximization(chinese_sentences, english_sentences, probabilities, num_iterations=10):
    """
    使用期望最大化算法训练IBM模型1。
    返回更新后的翻译概率字典。
    """

    for iteration in range(num_iterations):
        counts = {}
        total = {}

        for english_sentence, chinese_sentence in zip(english_sentences, chinese_sentences):
            for english_word in english_sentence:
                total[english_word] = 0

                for chinese_word in chinese_sentence:
                    total[english_word] += probabilities[english_word][chinese_word]

            for english_word in english_sentence:
                counts[english_word] = {}

                for chinese_word in chinese_sentence:
                    if english_word not in counts[english_word]:
                        counts[english_word][chinese_word] = 0
                    counts[english_word][chinese_word] += probabilities[english_word][chinese_word] / total[english_word]

                for chinese_word in probabilities[english_word]:
                    if chinese_word not in counts[english_word]:
                        counts[english_word][chinese_word] = 0

        for english_word in probabilities:
            for chinese_word in probabilities[english_word]:
                probabilities[english_word][chinese_word] = counts[english_word][chinese_word] / sum(counts[english_word].values())

    print("probabilities:",probabilities)

    return probabilities


def align_sentences(chinese_sentence, english_sentence, probabilities):
    """
    使用学习到的翻译概率对齐一对汉英句子。
    返回一个包含对齐结果的列表，其中每个元素为一个元组，包含汉语词语和对应的英语词语。
    """
    alignments = []

    for chinese_word in chinese_sentence:
        max_probability = 0
        best_english_word = None

        for english_word in english_sentence:

            probability = probabilities[english_word][chinese_word]

            if probability > max_probability:
                max_probability = probability
                best_english_word = english_word

        if best_english_word is not None:
            alignments.append([chinese_word, best_english_word])
    print("alignments :",alignments)

    return alignments


def evaluate_alignment(chinese_sentences, english_sentences, probabilities):
    """
    对给定的句子对进行词语对齐，并计算对齐质量。
    返回正确对齐的词语数量和总词语数量的比例。
    """
    num_correct_alignments = 0
    total_words = 0

    for chinese_sentence, english_sentence in zip(chinese_sentences, english_sentences):
        alignments = align_sentences(chinese_sentence, english_sentence, probabilities)
        i=0
        # word_list=english_sentence.split()
        for alignment in alignments:
            # print(len(english_sentence))
            chinese_word, english_word = alignment
            # print(type(english_sentence))

            if i < len(english_sentence):
                if english_word==english_sentence[i]:
                    num_correct_alignments += 1

            i+= 1

        total_words += len(chinese_sentence)

    alignment_quality = num_correct_alignments / total_words if total_words > 0 else 0

    return alignment_quality


# 加载数据
chinese_sentences, english_sentences = load_data('new_en-zh.txt')

# 抽样50万样例作为训练数据
#sample_size = 500000
sample_size = 2
chinese_sentences = chinese_sentences[:sample_size]
english_sentences = english_sentences[:sample_size]

# 初始化翻译概率
probabilities = initialize_probabilities(chinese_sentences, english_sentences)

# 使用EM算法训练IBM模型1
num_iterations = 1
probabilities = expectation_maximization(chinese_sentences, english_sentences, probabilities, num_iterations)

# 评估对齐质量
alignment_quality = evaluate_alignment(chinese_sentences, english_sentences, probabilities)
print(f"Alignment Quality: {alignment_quality}")
