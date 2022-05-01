# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:51:55 2022

@author: hvtga
"""

def extend_chain(super_list, dll, narrow=True):
    '''
    该函数在原有向链表的基础上
    按dll向下延长一次
    narrow参数:
    决定是否继承向链表中无法继续有向延长的元素(狭义的)
    
    input: 父向链表(double_list), dll
    output: 延长一元素的子向链表
    '''
    
    if narrow:
        sub_list = []
        for ele_li in super_list:
            for ext_ele in dll.__getitem__(ele_li[-1]):
                if ext_ele in ele_li:
                    continue
                else:
                    derive_li = ele_li.copy()
                    derive_li.append(ext_ele)
                    sub_list.append(derive_li)
            
        return sub_list
    else:
        sub_list = []
        for ele_li in super_list:
            if set(ele_li).issuperset(set(dll.__getitem__(ele_li[-1]))):
                derive_li = ele_li.copy()
                sub_list.append(derive_li)
            else:
                for ext_ele in dll.__getitem__(ele_li[-1]):
                    if ext_ele in ele_li:
                        continue
                    else:
                        derive_li = ele_li.copy()
                        derive_li.append(ext_ele)
                        sub_list.append(derive_li)
            
        return sub_list
        


def get_min_chain_li(dll, dot, simplified=True):
    '''
    该函数求得点链表中的单点最小闭包元
    simplified函数:
    决定返回的最小闭包元列表是否为最简
    '''
    
    chain_li = [[dot]]
    destin_li = dll[dot]
    next_chain_li = extend_chain(chain_li, dll, False)
    define = True
    re_li = []
    while define:
        chain_li = next_chain_li
        next_chain_li = extend_chain(chain_li, dll, False)
        
        for chain in next_chain_li:
            last_dot = chain[-1]
            if last_dot in destin_li:
                re_li.append(chain)
                define = False
    
    if simplified:
        simp_set = []
        for i in range(len(re_li)):
            add_chain = set(re_li.pop())
            if add_chain not in simp_set:
                simp_set.append(add_chain)
        return list(map(list, simp_set))
    else:
        return re_li
    
    
    
def get_all_cells_li(dll):
    '''
    返回点链表中所有点的闭包元列表
    '''
    re_li = []
    for i in range(len(dll)):
        re_li.append(get_min_chain_li(dll, i))
    
    return re_li


def get_basis_cells(dll):
    '''
    

    Parameters
    ----------
    dll : dll(list)
        输入dll

    Returns
    -------
    re_li : list(2d)
        输出该dll的基闭包列表

    '''
    all_cells_li = get_all_cells_li(dll)
    re_li = []
    for one_dot_cells in all_cells_li:
        one_dot_cells_cp = one_dot_cells.copy()
        for i in range(len(one_dot_cells)):
            add_cell = one_dot_cells_cp.pop()
            if add_cell not in re_li:
                re_li.append(add_cell)
    return re_li
            

def judge_penetration(dll, start, end):
    '''
    该函数用以判断在dll中,
    start点和end点是否贯通,
    如果贯通, return 0
    否则, return -1
    '''
    chain_start_li = [[start]]
    chain_end_li = [[end]]
    
    permit_next_s = True
    permit_next_e = True
    while permit_next_s or permit_next_e:
        
        for s_chain in chain_start_li:
            s_last_dot = s_chain[-1]
            s_last_dot_links = dll[s_last_dot]
            for e_chain in chain_end_li:
                e_last_dot = e_chain[-1]
                if e_last_dot in s_last_dot_links:
                    return 0
        
        if permit_next_s:
            next_chain_start_li = extend_chain(chain_start_li, dll)
            if next_chain_start_li == chain_start_li:
                permit_next_s = False
            else:
                chain_start_li = next_chain_start_li
        if permit_next_e:
            next_chain_end_li = extend_chain(chain_end_li, dll)
            if next_chain_end_li == chain_end_li:
                permit_next_e = False
            else:
                chain_end_li = next_chain_end_li
                
    return -1
            
        
                
        

def get_identity_cells_li(dll):
    '''
    该函数用于获得dll的基闭包元的同一性,
    返回同一基闭包元列表.
    即, 对所有具有同一性的基闭包元, 放置在同一列表内

    '''
    
    re_li = []
    basis_cells = get_basis_cells(dll)
    
    while basis_cells:
        main_id_cell = basis_cells[0]
        re_li_li = []
        re_li_li.append(basis_cells.pop(0))
        index = 0
        while index < len(basis_cells):
            as_id_cell = basis_cells[index]
            if len(main_id_cell) == len(as_id_cell):
                if set(as_id_cell).isdisjoint(set(main_id_cell)):
                    for main_ele in main_id_cell:
                        for as_ele in as_id_cell:
                            if judge_penetration(dll, main_ele, as_ele)+1:
                                define = True
                            else:
                                define = False
                                index +=1
                else:
                    define = True
                if define:
                    re_li_li.append(basis_cells.pop(index))
            else:
                 index += 1
        re_li.append(re_li_li)
    
    return re_li
                    
    
    
    
    
if __name__ == '__main__':
    dll = [[1,2,4,5],
           [0,3,6],
           [0,3],
           [1,2,4],
           [0,3,5,6],
           [0,4,6],
           [1,4,5],
           [8],
           [7]]

    basis_cells = get_basis_cells(dll)
    identity_cells = get_identity_cells_li(dll)


            
            
        
        
    
