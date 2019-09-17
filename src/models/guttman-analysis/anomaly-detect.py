# Detect the anomaly, able to detect either row/ column.
# The input is assumed to be sorted, with both row sorted(from good performance student to poor performance studet)
# and column sorted (good performance item and poor performance item).
# input: The input format is assumed to be a 2-d matrix/ array, with each cell representing the score (0/1/2/3..)

# For testing purpose, the 2-d matrix will be a 4*4 matrix, initialised with ones and zeros.
# The element of the inner array is the result of a student.

import pandas as pd
import copy
import math
import numpy
from numpy import dot
from numpy.linalg import norm


def detectDimenstion(matrix):
    """
    Return a tuple of dimension of the 2-d matrix.
    The first element is the number of student, the second number is the number of items.
    :param matrix: the 2-d matrix of Guttman Chart
    :return: A tuple containing the number of student and numebr of items.
    """
    return (matrix.__len__(), matrix[0].__len__())


# Calculate the summation of student score.
def sumStudentScore(matrix):
    """
    Summation of student total scores.
    :param matrix: the original data.
    :return: list that containing each students' scores.
    """
    return list(map(sum, matrix))


def sumItemScore(matrix):
    """
    Summation of item scores.
    :param matrix:  The original data.
    :return:    List that containing each column's scores.
    """
    result = []
    for i in range(len(matrix[0])):
        sum_item = sum([row[i] for row in matrix])
        result.append(sum_item)
    return result


# In case the user accidently provides an unsorted Guttman Chart, sort the chart based on student first.
def sortBasedOnStudent(matrix, studentSum):
    """
    Sort the original data/matrix, in case the user uploads an unsorted data.
    This sort is based on the student performance/scores.
    :param matrix:  The original data.
    :param studentSum:  List of Summation of student scores.
    :return:    The original data after sorting.
    """
    # matrix.sort(key = lambda x: x[len(matrix)-2])
    result = [x for (y, x) in sorted(zip(studentSum, matrix), key=lambda pair: pair[0])]
    return list(reversed(result))


# Receive a real_matrix (with student and item summation appended)
def sortBasedOnItem(matrix, itemSum):
    """
    Sort the original data/matrix, in case the user uploads an unsorted data.
    This sort is based on the item/column performace/scores.
    :param matrix:  The original data.
    :param itemSum:  List of Summation of student scores.
    :return:    The original data after sorting.
    """
    index = list(range(len(itemSum)))
    sublist_item = list(zip(itemSum, index))
    sublist_item = sorted(sublist_item, key=lambda x: x[0], reverse=True)  # Order that the inner list should follow.
    sorted_item_order = [x[1] for x in sublist_item]
    result = copy.deepcopy(matrix)
    for i in range(len(itemSum)):
        temp_student = list(zip(sorted_item_order, result[i]))
        temp_student = sorted(temp_student, key=lambda x: x[0])
        temp_student_list = [x[1] for x in temp_student]
        result[i] = temp_student_list
    return result


# Can return either the median of the students scores, or the median of the items.
def cal_median(matrix, summation):
    """
    Helper function. Not used for now. It will be used in the next phase, when dividing the partitions
    It calculate the median of summation list.
    :param matrix:  null
    :param summation: A list of summations
    :return:  The median of the summations
    """
    if len(summation) % 2 == 0:
        median = summation[int(len(summation) / 2)] + summation[int(len(summation) / 2) - 1]
        return median / 2
    else:
        median = summation[math.floor(len(summation) / 2)]
        return median


def cal_average(matrix, summation, number):
    """
    Can return either the average of the students scores, or the average score of the items.
    Not used for now, maybe useful for later usage.
    :param matrix: null
    :param summation:   A list of summation.
    :param number:  Number of element in summation.
    :return:    Average of the summation.
    """
    return sum(summation) / number


# Return the average score of item, per student.
def retrieve_average_per_item(matrix, itemsum):
    """
    Retrieve the average of the summation, per student.
    :param matrix:  The original input matrix data.
    :param itemsum: Either studentSum or itemSum
    :return:    Average
    """
    # Initialise a matrix to store items average results. len(matrix) is the number of student.
    result = []
    for i in range(len(itemsum)):
        result.append(itemsum[i] / len(matrix))
    return result


# This will be helpful for later use.
def transpose_matrix(matrix):
    """
    Transpose of the input matrix. The output is a 2-d/ nested list, but with row: items  and column: students.
    This function doesn't modify the original data, except the format(performa a transpose function on the original data)
    :param matrix:  The original input data.
    :return:    The original input data after performing transpose.
    """
    result = [list(x) for x in zip(*matrix)]
    print(result)
    return result


def retrieve_correlation_columns(matrix):
    """
    Retrieve the correlation between each column. This function utilises cal_correlation_items
    :param matrix:  The transposed matrix, that has the same data but expressed in the different way (to simplify calculation)
    :return:    A list of correlation calculated.
    """
    result = []
    for i in range(len(matrix)):
        result.append(cal_correlation_items(matrix, i))
    return [j for i in result for j in i]


def cal_correlation_items(matrix, current_index):
    """
    Calculate the correlation between each column. For now this function is implemented as this column, the column before
    it, the column after it. A more sensible way of doing it will be updated later(to calculate a range of columns).
    :param matrix: The transposed matrix, that has the same data but expressed in the different way (to simplify calculation)
    :param current_index: Current index of the column
    :return: A list of correlation calculated.
    """
    # If the row you want to check is the first column or the last column, only check the column after it or before it.
    result = []
    if current_index == 0:
        result.append(numpy.corrcoef(matrix[current_index], matrix[current_index + 1])[0, 1])
    elif current_index == len(matrix) - 1:
        result.append(numpy.corrcoef(matrix[current_index], matrix[current_index - 1])[0, 1])
    else:
        temp = numpy.corrcoef(matrix[current_index],
                              matrix[current_index + 1])[0, 1] + numpy.corrcoef(
            matrix[current_index], matrix[current_index - 1])[0, 1]
        result.append(temp / 2.0)
    return result


def detect_item_irregular(similarity1, similarity2):
    """
    Detect if the column/item is irregular. If it is irregular, append its position to the list.
    If the average score of the two lists are smaller than 0.5(for now, I don't know how good the data will be, let's try 0.5 for now)
    This parameter will change as development goes.
    :param similarity1: Similarity calculated between each column.
    :param similarity2: Similarity calculated between each column and the whole table(student data)
    :return: the list of index/position that is irregular
    """
    average_sim = [(x + y) / 2 for (x, y) in zip(similarity1, similarity2)]
    result = []
    for i in range(len(average_sim)):
        if average_sim[i] < 0.5:
            result.append(i)
    return result


# [0.8838834764831843, 0.7306168728364051, 0.5773502691896258, 0.5773502691896258]
# [0.9503288904374105, 0.8696263565463042, 0.8215838362577491, 0.4743416490252569]
def similarity_between_columns(matrix):
    """
    Calculate the similarity between one column with the column before it and after it. This calculation is based on cosine,
    which generated by dot product divided by normalised production.
    :param matrix: The transposed matrix, that has the same data but expressed in the different way (to simplify calculation)
    :return: A list of similarities of each column/item.
    """
    similarity = []
    for i in range(len(matrix)):
        if i == 0:
            cosine = dot(matrix[i], matrix[i + 1]) / (norm(matrix[i]) * norm(matrix[i + 1]))
        elif i == len(matrix) - 1:
            cosine = dot(matrix[i], matrix[i - 1]) / (norm(matrix[i]) * norm(matrix[i - 1]))
        else:
            cosine1 = dot(matrix[i], matrix[i + 1]) / (norm(matrix[i]) * norm(matrix[i + 1]))
            cosine2 = dot(matrix[i], matrix[i - 1]) / (norm(matrix[i]) * norm(matrix[i - 1]))
            cosine = (cosine1 + cosine2) / 2
        similarity.append(cosine)
    return similarity


def similarity_between_column_whole(matrix, ave_per_student):
    """
    Calculate the similarity between each column and the whole table(student average score). This calculation is based on cosine,
    which generated by dot product divided by normalised production.
    :param matrix:  The transposed matrix, that has the same data but expressed in the different way (to simplify calculation)
    :param ave_per_student: The average score each column, per student.
    :return: A list of similarities of each column/item.
    """
    similarity = []
    for i in range(len(matrix)):
        cosine = dot(matrix[i], ave_per_student) / (norm(matrix[i]) * norm(ave_per_student))
        similarity.append(cosine)
    return similarity

# Not implemented yet. Ideally should work under the 'Fou Partition' detection.
def detect_student_irregular(matrix):
    print("hello")



# def appendStudentSum(matrix):
#     result = list(sumStudentScore(matrix))
#     print(matrix.__len__())
#     real_matrix = copy.deepcopy(matrix)
#     real_matrix.append(result)  # Student result is appended.
#     return real_matrix
# def appendItemSum(original_matrix, real_matrix):
#     result = sumItemScore(original_matrix)
#     real_matrix.append(result)
#     return real_matrix


# TODO: 我认为这个算法可以分为三部分： 1. detect周围的correlation(1-2个?)，correlation 的比值应该小于 多少多少，这个比值应该调参，目前来说还不知道。 correlation部分应该占比1/2
# TODO： 2. 计算当前item与整体items的similarty， 用cosine夹角计算。 占比1/2
# TODO: 3. 四分之一法，暴力规划四部分区域大小， 检测有无异常行为。 这部分占比小，但是如果检测出来，就应该加一个flag， 告诉之前的算法，当前item有存在不合格风险。

# TODO: RoadMap : We can treate the problem as a anomaly detection problem and apply outelier detection algorithms, including
# TODO: 基于密度异常点检测 / 基于邻近度异常点检测等等。 Isolation Forest看起来是个不错的选择。 而且Isolation Forest 在sklearn有实现，调包可完成。

# 'Four Partition'

'''
According to the median of the items and students numbers, as well as students performance, 
The following 'Four Partitions' algorithm is implemented. 
Since the counter will start from the top left, block 'A' will be the most compentent student, answerign the easiest items/questions. 
This block tend to have a low percentage of false. If detect a zero/false, falge this student and this items. Even though it may 
not effect the total correlation performace, the anomaly shows that there is unusual/odd zero. 
Similarly, the percentage of block 'B' and block 'C', containing zeros/false will be higher than blcok 'A'. Detection in these
two areas will not flag the student or items. The flags will be raised only if the anomaly 

          |  
    A     |    B
          |  
          |
---------- ----------
          |  
    C     |    D     
          |  
          |


'''

'''
Driver function. Test data is Matrix(probably not a good idea) 
'''
def main():
    Matrix = [[0, 1, 1, 1], [1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 0, 0], [1, 2, 0, 0]]
    print(Matrix)
    studentSum = sumStudentScore(Matrix)
    itemSum = sumItemScore(Matrix)
    print(studentSum)
    print(itemSum)
    sortedMatrixStudent = sortBasedOnStudent(Matrix, studentSum)  # After sorting based on student summation.
    sortedMatrixItem = sortBasedOnItem(sortedMatrixStudent, itemSum)  # After sorting based on item summation.
    matrix = sortedMatrixItem
    print("After sorting:", matrix)

    # After sorting the data, both item_summation and student_summation records should be sorted.
    # Keep the original order unchanged.
    student_sum_copy = copy.deepcopy(studentSum)
    item_sum_copy = copy.deepcopy(itemSum)
    student_sum_copy.sort()
    item_sum_copy.sort()
    student_sum_copy = list(reversed(student_sum_copy))
    item_sum_copy = list(reversed(item_sum_copy))

    # The four variables below are not used for now, but maybe useful for later partitions.
    student_score_median = cal_median(matrix, student_sum_copy)
    item_median = cal_median(matrix, item_sum_copy)
    student_score_ave = cal_average(matrix, student_sum_copy, len(studentSum))
    item_ave = cal_average(matrix, item_sum_copy, len(itemSum))

    ave_per_item = retrieve_average_per_item(matrix, item_sum_copy)  # Average of each column. Sorted list.
    ave_per_student = retrieve_average_per_item(matrix, student_sum_copy)
    items_in_matrix = transpose_matrix(matrix)

    #####################################################################################
    # This is the result to return back to the server, a list of correlation, in the order with each columns.
    correlation_of_columns = retrieve_correlation_columns(items_in_matrix)


    # Two lists containing similarities. Inputs are items/criteria inputs, not student matrix(not the original data).
    columns_similarity = similarity_between_columns(items_in_matrix)
    columns_whole_similarity = similarity_between_column_whole(items_in_matrix, ave_per_student)

    #####################################################################################
    # This list should be returned to the server, a list of irregular columns.
    # This list contains the position of irregular columns.
    irregular_column_items = detect_item_irregular(columns_similarity, columns_whole_similarity)


if __name__ == '__main__':
    main()


###############################################################################
####### Any code bleow this line are depreciated(the use of pandas)
###############################################################################
###############################################################################
####### Any code bleow this line are depreciated(the use of pandas)
###############################################################################
###############################################################################
####### Any code bleow this line are depreciated(the use of pandas)
###############################################################################
###############################################################################
####### Any code bleow this line are depreciated(the use of pandas)
###############################################################################
# Another way of using Pandas. The following code will clean and sort the data.
# Sample Format:
#             student0  student1  student2  student3  student4  ItemSum
# item0            1.0       1.0       1.0       1.0       1.0      5.0
# item1            1.0       1.0       1.0       1.0       2.0      6.0
# item2            1.0       1.0       1.0       0.0       0.0      3.0
# item3            1.0       0.0       0.0       0.0       0.0      1.0
# StudentSum       4.0       3.0       3.0       2.0       3.0      NaN
# test = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0], [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], [1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1]]
# test_data = [[1],[0],[1],[0],]

def formatData(matrix):
    studentName = []
    for i in range(len(matrix)):
        studentName.append(str(i))
    data = dict(zip(studentName, matrix))

    data_pd = pd.DataFrame(data, retrieveIndexOfItems(matrix))
    # data_pd.loc['StudentSum'] = sumStudentScore(matrix)
    additional = pd.DataFrame({'ItemSum': sumItemScore(matrix)}, retrieveIndexOfItems(matrix))  # Add column
    result = pd.concat([data_pd, additional], axis=1, sort=True)
    lis = sumStudentScore(matrix)
    lis.append(None)
    result.loc['StudentSum'] = lis  # Add addtional row
    return result


def retrieveIndexOfItems(matrix):
    item_name = []
    for i in range(len(matrix[0])):
        item_name.append(str(i))
    return item_name


def sortStudentandItems(data):
    data = data.sort_values(by=['ItemSum'], ascending=False)
    # print(data)
    data = data.sort_values(by='StudentSum', axis=1, ascending=False)
    # print(data)
    return data


# These two functions will return the headers for columns and rows after the data is sorted.
# The order of both columns and rows are sorted.
def retrieve_column_headers(data):
    return list(data.columns.values)


def retrieve_row_headers(data):
    return list(data.index)


# def sortStudent(matrix):
#     matrix.sort_values('')

# data = formatData(Matrix)
# # print(data)
# data= sortStudentandItems(data)
# data_list = [tuple(x) for x in data.to_records(index=True)]

# print(data_list)
# detectStudentIrregular(data)
# print("Correlation: ")
'''
Correlation: 
                   1         0         2         3  StudentSum
1           1.000000  0.979796  0.821584  0.580948    0.000000
0           0.979796  1.000000  0.894427  0.632456         NaN
2           0.821584  0.894427  1.000000  0.707107    0.645497
3           0.580948  0.632456  0.707107  1.000000    0.790569
StudentSum  0.000000       NaN  0.645497  0.790569    1.000000'''


# print(data.T.corr())
# The above correlation is not correct? Probably.

# This will return the correlation between each column.
# print(data['1'].corr(data['0']))
# print(data['1'].corr(data['4']))
# print(data['1'].corr(data['2']))
# print("Correlation between one column and multiple columns: ")
# print(data[['1','2','3','4']].corrwith(data['0']))

# print(retrieve_column_headers(data))
# print(retrieve_row_headers(data))
# row_header = retrieve_row_headers(data)
# column_header = retrieve_column_headers(data)

# data2 = formatData(test)
# print(data2)
# data2_sort = sortStudentandItems(data2)
# print(data2[data2.columns[1:]].corr()[:-1])
# print("test 2: Correlation between one column and multiple coluns: ")
# print(data2[['1','2','3','4','5','6','7','8','9','10','0','12']].corrwith(data2['11']))

# correlation = pd.DataFrame()
# for a in list('0'):
#     for b in list(data.columns.values):
#         correlation.loc[a,b] = data.corr().loc[a,b]

# print("Correlation")
# print(data2_sort['8'].corr(data2_sort['5']))
# print("data 12 ")
# print(data2_sort['10'])
# print(data2_sort['11'])
# print(data2_sort['1'])

def calculateRowCorrelation(data):
    # print(data.T.corr().unstack().reset_index(name="corr"))
    # print(data.T.corr())
    print()
# calculateRowCorrelation(data2_sort)