# -*- coding: utf-8 -*-
# @Time : 2022/08/15  5:30 下午
import os
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import auc, roc_curve

import matplotlib.pylab as plt


def computeTPFP(labels, predictions):
    ## 计算真假阳性
    TP = 0
    for i in range(0, len(labels)):
        if labels[i] == predictions[i] and labels[i] == 1:
            TP += 1
    print("True Positive: ", TP)

    FP = 0
    for i in range(0, len(labels)):
        if labels[i] == 0 and predictions[i] == 1:
            FP += 1
    print("False Positive: ", FP)

    TN = 0
    for i in range(0, len(labels)):
        if labels[i] == predictions[i] and labels[i] == 0:
            TN += 1
    print("True Negative: ", TN)

    FN = 0
    for i in range(0, len(labels)):
        if labels[i] == 1 and predictions[i] == 0:
           FN += 1
    print("False Negative: ", FN)

    CP = 0
    for i in range(0, len(labels)):
        if labels[i] == predictions[i]:
            CP += 1
    print("Correct Prediction: ", CP) # 3
    print(CP == TP + TN) # True

    ICP = 0
    for i in range(0, len(labels)):
        if labels[i] != predictions[i]:
            ICP += 1
    print("Incorrect Prediction: ", ICP)  # 7
    print(ICP == FP + FN)  # True
    return TP, FP, TN, FN


def computerMetricAPI(labels, predictions):
    ## 使用sklearn 计算acc, precision, recall, f1
    acc = accuracy_score(labels, predictions) * 100
    print("acc: ", acc)

    recall = recall_score(labels, predictions)
    print("recall: ", recall)

    precision = precision_score(labels, predictions) * 100
    print("precision: ", precision)

    f1 = f1_score(labels, predictions)
    print("f1: ", f1)
    return


def computerMetric(labels, predictions):
    TP, FP, TN, FN = computeTPFP(labels, predictions)

    ## 计算acc, precision, recall, f1
    accuracy = (TP + TN)/(TP + FP + TN + FN)
    print("acc: ", accuracy*100)

    recall = (TP)/(TP+FN)
    print("recall: ", recall*100)

    precision = TP/(TP+FP)
    print("precision: ", precision)

    f1 = 2*(precision * recall)/(precision + recall)
    print("f1: ", f1)
    return


def showConfusionMatrix(labels, predictions):
    """ 可视化混淆矩阵 """
    confusion = confusion_matrix(labels, predictions)
    FN = confusion[1][0]
    TN = confusion[0][0]
    TP = confusion[1][1]
    FP = confusion[0][1]
    confusion = confusion / (TP + FP + TN + FN)

    import seaborn as sns
    sns.heatmap(confusion, annot=True, xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
    plt.ylabel("Label")
    plt.xlabel("Predicted")
    # plt.show()
    plt.savefig("./figures/confusion_matrix.jpg")


    # plt.matshow(confusion, cmap=plt.cm.Reds) # 根据最下面的图按自己需求更改颜色
    # # plt.colorbar()
    #
    # for i in range(len(confusion)):
    #     for j in range(len(confusion)):
    #         plt.annotate(confusion[j, i], xy=(i, j), horizontalalignment='center', verticalalignment='center')
    #
    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')
    # plt.show()



if __name__ == '__main__':
    ## 数据GT label （0表示real, 1表示fake）
    labels = [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
    ## 数据pred label
    predictions = [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    pred = [0.2, 0.1, 0.8, 1.0, 0.9, 0.9, 0.01, 0.8, 0.9, 0.9, 0.9, 0.1, 0.8, 0.9, 0.8, 0.9, 1.0, 0.9, 0.8, 0.2]

    ## 计算指标数据
    computerMetric(labels=labels, predictions=predictions)

    ## 可视化混淆矩阵
    showConfusionMatrix(labels=labels, predictions=predictions)

    ## 计算auc
    fpr, tpr, thresholds = roc_curve(np.array(labels), np.array(pred), pos_label=1)
    au = auc(fpr, tpr)
    print("auc: ", au)