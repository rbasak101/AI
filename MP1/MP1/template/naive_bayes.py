# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

import math
from tqdm import tqdm
import reader
"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


"""
load_data calls the provided utility to load in the dataset.
You can modify the default values for stemming and lowercase, to improve performance when
    we haven't passed in specific values for these parameters.
"""
# False for all
def load_data(trainingdir, testdir, stemming=False, lowercase=True, silently=False):
    print(f"Stemming is {stemming}")
    print(f"Lowercase is {lowercase}")
    train_set, train_labels, dev_set, dev_labels = reader.load_dataset(trainingdir,testdir,stemming,lowercase,silently)
    return train_set, train_labels, dev_set, dev_labels


def print_paramter_vals(laplace,pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameter and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

def naiveBayes(train_set, train_labels, dev_set, laplace=0.001, pos_prior=0.8,silently=False):

    """
    P(T | W) = P(W | T) * P(T) / P(W)
    key: word, value: prob = P(W | T)
    P(W | T) = P(W & T) / P(T)
    train_set: List of list of words
        Ex: [["This", "is", "a", "gem", "of", "words", ....], ["Of", "the", ...], ... ]

    train_labels: 1 or 0.
        1 = Good review
        0 = Bad review

    get word count: Count number of times that word shows up in good or bad review accordingly
    low accuracy: get rid of filler words (Stop words) + use stemming

    """
    print_paramter_vals(laplace,pos_prior)
    # print("training set: ", train_set[0])
    # print("training first label: ", train_labels[0])
    # print("training set: ", train_set[-1])
    # print("training first label: ", train_labels[-1])
    # print("training labels: ", train_labels)

    # total_labels = total_pos_labels + total_neg_labels   # 8000 for training
    # prob_pos_label = total_pos_labels / total_labels
    # prob_neg_label = total_neg_labels / total_labels

    # filtered_train_set = remove_stop_words(train_set)
    # print("filted train set vs input train set: ", len(filtered_train_set), len(train_set))

    pos_words_freq, neg_words_freq, total_pos_labels, total_neg_labels, total_pos_words, total_neg_words = word_count_dict(train_set, train_labels)
    # pos_words_freq, neg_words_freq, total_pos_labels, total_neg_labels, total_pos_words, total_neg_words = word_count_dict(filtered_train_set, train_labels)
    

    # print(len(pos_words_freq), len(neg_words_freq))
    # print(total_pos_labels, total_neg_labels, total_pos_words, total_neg_words)


    V_pos = len(pos_words_freq)
    V_neg = len(neg_words_freq)
    yhats = []
    for doc in tqdm(dev_set, disable=silently): # for each review
        pos_prob_post = 0
        neg_prob_post = 0
        for word in doc:
            if word in pos_words_freq:
                pos_word_log_prob = math.log((pos_words_freq[word] + laplace) / (total_pos_words + laplace * (V_pos + 1)))
            else:
                pos_word_log_prob = math.log(laplace / (total_pos_words + laplace * (V_pos + 1)))  # P(UNK | C)
            pos_prob_post += pos_word_log_prob

            if word in neg_words_freq:
                neg_word_log_prob = math.log((neg_words_freq[word] + laplace) / (total_neg_words + laplace * (V_neg + 1)))
            else:
                neg_word_log_prob = math.log(laplace / (total_neg_words + laplace * (V_neg + 1)))
            neg_prob_post += neg_word_log_prob
        
        pos_prob_post += math.log(pos_prior)
        neg_prob_post += math.log(1 - pos_prior)

        if pos_prob_post > neg_prob_post:
            yhats.append(1)
        else:
            yhats.append(0)

    return yhats

def word_count_dict(train_set, train_labels):  # P(Word | Type)
    """
    Finding word freq for each word in positives and negatives and total number of positives and negative words
    """
    pos, neg = {}, {} 
    pos_num_labels, neg_num_labels = 0, 0
    total_pos_words, total_neg_words = 0, 0

    for i in range(len(train_set)):
        word_list = train_set[i]

        if train_labels[i] == 1:         # positive words
            pos_num_labels += 1
            for word in word_list:
                total_pos_words += 1
                if word not in pos:
                    pos[word] = 1
                else:
                    pos[word] += 1
                
        else:                           # negative words
            neg_num_labels += 1                         
            for word in word_list:
                total_neg_words += 1
                if word not in neg:
                    neg[word] = 1
                else:
                    neg[word] += 1


    return pos, neg, pos_num_labels, neg_num_labels, total_pos_words, total_neg_words


def remove_stop_words(train_set):
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    filtered_train_set = []
    for word_list in train_set:
        sub_list = []
        for w in word_list:
            if w not in stop_words:
                sub_list.append(w)
        filtered_train_set.append(sub_list)
    return filtered_train_set

def print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameters, model-mixture lambda parameter, and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

# main function for the bigrammixture model
# .015, .0037, 1.0, 0.8
def bigramBayes(train_set, train_labels, dev_set, unigram_laplace= 0.0003, bigram_laplace= 0.00601, bigram_lambda=.59,pos_prior=0.25, silently=False):
    print_paramter_vals_bigram(unigram_laplace,bigram_laplace,bigram_lambda,pos_prior)

    # UNIGRAM
    pos_words_freq, neg_words_freq, total_pos_labels, total_neg_labels, total_pos_words, total_neg_words = word_count_dict(train_set, train_labels)
    unigram_pos = []
    unigram_neg = []
    V_pos = len(pos_words_freq)
    V_neg = len(neg_words_freq)
    yhats = []
    for doc in tqdm(dev_set, disable=silently): # for each review
        pos_prob_post = 0
        neg_prob_post = 0
        for word in doc:
            if word in pos_words_freq:
                pos_word_log_prob = math.log((pos_words_freq[word] + unigram_laplace) / (total_pos_words + unigram_laplace * (V_pos + 1)))
            else:
                pos_word_log_prob = math.log(unigram_laplace / (total_pos_words + unigram_laplace * (V_pos + 1)))  # P(UNK | C)
            pos_prob_post += pos_word_log_prob

            if word in neg_words_freq:
                neg_word_log_prob = math.log((neg_words_freq[word] + unigram_laplace) / (total_neg_words + unigram_laplace * (V_neg + 1)))
            else:
                neg_word_log_prob = math.log(unigram_laplace / (total_neg_words + unigram_laplace * (V_neg + 1)))
            neg_prob_post += neg_word_log_prob
        
        pos_prob_post += math.log(pos_prior)
        neg_prob_post += math.log(1 - pos_prior)
        
        unigram_pos.append(pos_prob_post)
        unigram_neg.append(neg_prob_post)


    # pos_words_freq, neg_words_freq, total_pos_labels, total_neg_labels, total_pos_words, total_neg_words = word_count_dict(train_set, train_labels)
    # print("Words: ", total_pos_words, total_neg_words)
    # # print(len(train_set), train_set[0])
    pos_pair_freq, neg_pair_freq, pos_total_pairs, neg_total_pairs = pair_count_dict(train_set, train_labels)

    # BIGRAM
    yhats = []
    bigram_pos = []
    bigram_neg = []
    V_pos = len(pos_pair_freq)
    V_neg = len(neg_pair_freq)
    for doc in tqdm(dev_set,disable=silently):
        pos_prob_post = 0
        neg_prob_post = 0
        for i in range(1, len(doc)):
            word1, word2 = doc[i - 1], doc[i]
            if (word1, word2) in pos_pair_freq:
                pos_pair_log_prob = math.log((pos_pair_freq[(word1, word2)] + bigram_laplace) / (pos_total_pairs + bigram_laplace * (V_pos + 1)))
            else:
                pos_pair_log_prob = math.log(bigram_laplace / (pos_total_pairs + bigram_laplace * (V_pos + 1)))  # P(UNK | C)
            pos_prob_post += pos_pair_log_prob


            if (word1, word2) in neg_pair_freq:
                neg_pair_log_prob = math.log((neg_pair_freq[(word1, word2)] + bigram_laplace) / (neg_total_pairs + bigram_laplace * (V_neg + 1)))
            else:
                neg_pair_log_prob = math.log(bigram_laplace / (neg_total_pairs + bigram_laplace * (V_neg + 1)))  # P(UNK | C)
            neg_prob_post += neg_pair_log_prob

        pos_prob_post += math.log(pos_prior)
        neg_prob_post += math.log(1 - pos_prior)

        bigram_pos.append(pos_prob_post)
        bigram_neg.append(neg_prob_post)

    for i in range(len(dev_set)):
        positive_posterior = (1 - bigram_lambda) * unigram_pos[i] +  (bigram_lambda) * bigram_pos[i]
        negative_posterior = (1 - bigram_lambda) * unigram_neg[i] +  (bigram_lambda) * bigram_neg[i]

        if positive_posterior > negative_posterior:
            yhats.append(1)
        else:
            yhats.append(0)

    return yhats




def pair_count_dict(train_set, train_labels):
    pos_pair_freq, neg_pair_freq = {}, {}
    pos_total_pairs, neg_total_pairs = 0, 0
    total_words = 0
    pos_num_labels, neg_num_labels = 0, 0
    for i in range(len(train_set)):
        word_list = train_set[i]
        total_words += len(train_set[i])
        if train_labels[i] == 1:
            pos_num_labels += 1
            for j in range(1, len(word_list)):
                pos_total_pairs += 1
                word1, word2 = word_list[j - 1], word_list[j]
                if (word1, word2) not in pos_pair_freq:
                    pos_pair_freq[(word1, word2)] = 1
                else:
                    pos_pair_freq[(word1, word2)] += 1
        else:
            neg_num_labels += 1
            for j in range(1, len(word_list)):
                neg_total_pairs += 1
                word1, word2 = word_list[j - 1], word_list[j]
                if (word1, word2) not in neg_pair_freq:
                    neg_pair_freq[(word1, word2)] = 1
                else:
                    neg_pair_freq[(word1, word2)] += 1
    
    # print("Total words: ", total_words)
    # print("Total pairs: ", pos_total_pairs, neg_total_pairs, pos_num_labels, neg_num_labels, pos_total_pairs + pos_num_labels, neg_total_pairs + neg_num_labels)
    # print(pos_pair_freq, neg_pair_freq)
    return pos_pair_freq, neg_pair_freq, pos_total_pairs, neg_total_pairs