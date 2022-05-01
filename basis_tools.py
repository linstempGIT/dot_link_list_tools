# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:08:13 2022

本脚本探讨了给定点链表时,
判定该matrix的正确性
同时给定该点链表在欧式空间内的存在性
并求得其最小划分矩阵

@author: hvtga
"""

from itertools import permutations, combinations
from math import factorial


# 0 is blue, 1: green, 2: red, 3: yellow, 4: None
all_colors = [0, 1, 2, 3, 4]

def links_num(dots_links_list):
    '''
    Parameters
    ----------
    dots_links_list : list
        输入点链表.

    Returns
    -------
    links_num_list : list
        返回各点链数列表.

    '''
    links_num_list = []
    for dot in dots_links_list:
        links_num_list.append(len(dot))
    return links_num_list

def links2color_map_func(color_list, links_list):
    re_li = []
    for dot in links_list:
        re_li.append(color_list[dot])
    return re_li
        
def need_less_colors(dots_links_list):
    '''
    Parameters
    ----------
    dots_links_list : list
        输入点链矩阵.

    Returns
    -------
    nlc_list : list
        返回该点链矩阵的最简区别矩阵.

    '''
    len_dll = len(dots_links_list)
    nlc_list = [8] * len_dll
    nlc_list[0] = 0
    # nlc_list[1] = 1
    
    for dot in range(1, len_dll):
        links_list = dots_links_list[dot]
        links_colors_list = links2color_map_func(nlc_list, links_list)
        links_colors_set = set(links_colors_list)
        for color in all_colors:
            if not color in links_colors_set:
                nlc_list[dot] = color
                break
    return nlc_list

# Eliminate negative dots
# 该函数用以剔除消极点
# 剔除每点链点数小于n的消极点
def elm_neg_dot(dots_links_list, n):
    
    dll_copy = []
    neg_dots_list = []
    links_num_list = links_num(dots_links_list)
    for index, dot_links_num in enumerate(links_num_list):
        if dot_links_num > n:
            dot_links_list_copy = dots_links_list[index].copy()
            dll_copy.append(dot_links_list_copy)
        else:
            neg_dots_list.append(index)
            dll_copy.append([])          
         
    for index, dot_links_list in enumerate(dll_copy):
        for neg_dot in neg_dots_list:
            if neg_dot in dot_links_list:
                dot_links_list.remove(neg_dot)
     
    if links_num_list == list(filter(lambda x: x>n or x==0, links_num_list)):
        return dll_copy

    else:
        return elm_neg_dot(dll_copy, n)
'''
def elm_neg_dot(dots_links_list, n):
    links_num_list = links_num(dots_links_list)
    return elm_neg_dot_part(dots_links_list, n, links_num_list)
'''    
            
# 该函数用于检查点链表在欧几里得空间是否存在
def inspect(dots_links_list):
    '''
    该函数用于检查点链表是否合理,
    点链表少于一点, return -1
    dll第n点的链点数于被链数不等, return -2
    正常返回0
    ''' 
    # 点链表至少有一个点
    if not list(filter(lambda x: x, dots_links_list)):
        return -1               # 至少有一个点
    # 第n点的链点数与该点被链点数相等
    dots_links_num = links_num(dots_links_list)
    for index_ln, dot_links_num in enumerate(dots_links_num):
        count = 0
        for index_ll, dot_links_list in enumerate(dots_links_list):
            if index_ln == index_ll:
                if index_ll in dot_links_list:
                    return -1                  # 本点链点包含本点
            else:             
                if index_ln in dot_links_list:
                    count += 1
        if count != dot_links_num:
            
            return -2      # 第n点的链点数与该点被链点数不相等
    return 0
        
 
# 将nn(n>=4)相链的点链表判错
def nnconnect(dots_links_list):
    '''
    该函数判断dll中是否存在nn(n>=4)相链:
        如果存在nn相链, return -1
        不存在,则return0
    '''
    re_dll = list(filter(lambda x: x, elm_neg_dot(dots_links_list, 3)))
    #dots_links_num = links_num(re_dll)
    #len_re_dll = len(re_dll)
    re_re_dll = []
    for index, dot_links_list in enumerate(re_dll):
        re_re_dll.append(re_dll[index].copy())
        re_re_dll[index].append(index)
    for dot in re_re_dll:
        judge = 0
        set_dot = set(dot)
        for connect_dot in dot[:-1]:        
            set_connect_dot = set(re_re_dll[connect_dot])
            if set_dot == set_connect_dot or\
                set_dot.issubset(set_connect_dot) or\
                set_connect_dot.issubset(set_dot):
                    continue
            else:
                judge = 1
                break
        if judge == 0:
            return -1                     # 存在nn相链
    return 0                   # 不存在nn相链

# 将点链表转换为全链表
def chage_dll2all(dll):
    pass    

        
# 将给定的点链表进行换序转置
def change_dll(dll, change_seq):
    changed_dll = []
    mark_list = []
    for seq in change_seq:
        changed_dll.append(dll[seq].copy())
    links_num_list = links_num(changed_dll)
    for link_num in links_num_list:
        mark_list.append([0] * link_num)
    for index_cs, seq in enumerate(change_seq):
        for index_cd, dot in enumerate(changed_dll):
            for index_ld, link_dot in enumerate(dot):
                if seq == link_dot and mark_list[index_cd][index_ld] == 0:
                    dot[index_ld] = index_cs
                    mark_list[index_cd][index_ld] = 1
                    continue
    
    if mark_list == list(filter(lambda x: set(x)=={1}, mark_list)):
        return changed_dll
    else:
        return -1
                    

# 得到点链表的换序全排列
def get_changeSeq_P(dll, n):
    re_li = []
    index_dll = list(range(len(dll)))
    changeSeq_choise_list = list(combinations(index_dll,n))
    
    for choise_tp in changeSeq_choise_list:
        unchange_list = []
        changed_list = []
        for index_dot in index_dll:
            if index_dot in choise_tp:
                unchange_list.append(-1)
            else:
                unchange_list.append(index_dot)
        
        P_choise_li = list(permutations(choise_tp))[:-1] 
        for choise_tp in P_choise_li:
            choise_li = list(choise_tp)
            changed_li_part = []
            for index in unchange_list:
                if index == -1:
                    changed_li_part.append(choise_li.pop())
                else:
                    changed_li_part.append(index)
            changed_list.append(changed_li_part)
            
        # changed_list是一个组合数的全排列的换序列表
        # re_li是所有组合数的所有排列换序列表
        re_li.append(changed_list)
    
    # re_li理论上有共C(n, len(dll))*(P(n,n) - 1)种
    return re_li
    #changeSeq_list = list(permutations(changeSeq_choise_list))
    
    
def def_exist_inN2(dll):
    '''
    该函数用于判断dll在二维空间中
    是否存在, 如果存在, 返回0, 否则, 返回-1
    '''
    if inspect(dll)+1 and nnconnect(dll)+1:
        return 0
    else:
        return -1
    
'''
def main():
    lines = []
    while True:
        try:
            lines.append(list(map(int, input().split())))
        except:
            break
    dots_links_list = lines.copy()
    
    inspect_result = inspect(dots_links_list)
    if inspect_result == 0:
        if (nnconnect(dots_links_list)+1):
            print("need less colors:", need_less_colors(dots_links_list))
        else:
            print("The point linked list does not exist in Euclidean space.")
    else:
        print("Error points-links-list")
'''

'''
def main(n=5):
    A = [[2,3,4,5,6,7,8],
         [2,3,4,5,6,7,8],
         [0,1,3,8],
         [0,1,2,4],
         [0,1,3,5],
         [0,1,4,6],
         [0,1,5,7],
         [0,1,6,8],
         [0,1,2,7]]
    get = get_changeSeq_P(A, n)
    cmn = factorial(len(A)) // (factorial(n) * factorial((len(A)-n)))
    
    try:
        with open('./cp_A_5.txt', 'w') as f:
            for i in range(cmn):
                title = f"第n种组合数:{i:d}\n"
                f.write(title)
                write_i = str(get[i])+'\n'
                f.write(write_i)
    except:
        print("errro")
'''

def main():
    A = [[2,3,4,5,6,7,8],
         [2,3,4,5,6,7,8],
         [0,1,3,8],
         [0,1,2,4],
         [0,1,3,5],
         [0,1,4,6],
         [0,1,5,7],
         [0,1,6,8],
         [0,1,2,7]]
    get = get_changeSeq_P(A, 2)
    for i in get:
        for x in i:
            print(need_less_colors(change_dll(A, x)))
    

if __name__ == '__main__':
    main()
