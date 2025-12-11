#ifndef LINKLIST_H
#define LINKLIST_H

#include "common.h"  // 包含ElemType定义、bool等

// 单链表节点结构体（不带头节点，考研主流场景）
typedef struct node {
    ElemType data;      // 数据域
    struct node* next;  // 指针域（指向下一个节点）
} LNode, *Linklist;     // LNode：节点类型；Linklist：头指针类型（无额外头节点）

// 1. 初始化单链表（不带头节点，空表=头指针置NULL）
// 参数：L-头指针的指针（二级指针，需修改头指针）
// 返回：成功true，失败false（参数为NULL）
bool Linklist_Init(Linklist* L);

// 2. 创建单个节点
// 参数：data-节点数据域值
// 返回：成功返回节点指针，失败返回NULL（内存分配失败）
LNode* Linklist_CreatNode(ElemType data);

// 3. 判断链表是否为空（不带头节点：L==NULL即为空）
// 参数：L-头指针（一级指针，仅读取）
// 返回：空表true，非空false
bool Linklist_IsEmpty(Linklist L);

// 4. 求链表长度（节点个数，不包含头节点）
// 参数：L-头指针（一级指针）
// 返回：链表长度（空表返回0）
int Linklist_Length(Linklist L);

// 5. 按位置查找节点（pos从1开始，不带头节点）
// 参数：L-头指针；pos-目标位置；data-输出参数（存储节点数据，不可为NULL）
// 返回：成功返回节点指针，失败返回NULL（pos非法/空表）
LNode* Linklist_GetPos(Linklist L, int pos, ElemType* data);

// 6. 按值查找节点（返回第一个匹配节点，不带头节点）
// 参数：L-头指针；val-目标值
// 返回：成功返回节点指针，失败返回NULL（无匹配值/空表）
LNode* Linklist_GetVal(Linklist L, ElemType val);

// 7. 按位置插入节点（pos从1开始，插入到pos位置，不带头节点）
// 参数：L-头指针的指针；pos-插入位置（1<=pos<=length+1）；data-节点数据
// 返回：成功true，失败false（pos非法/内存分配失败）
bool Linklist_InsertPos(Linklist* L, int pos, ElemType data);

// 8. 头插法插入节点（直接插表头，不带头节点）
// 参数：L-头指针的指针；data-节点数据
// 返回：成功true，失败false（内存分配失败）
bool Linklist_InsertHead(Linklist* L, ElemType data);

// 9. 尾插法插入节点（直接插表尾，不带头节点）
// 参数：L-头指针的指针；data-节点数据
// 返回：成功true，失败false（内存分配失败）
bool Linklist_InsertTail(Linklist* L, ElemType data);

// 10. 按位置删除节点（pos从1开始，不带头节点）
// 参数：L-头指针的指针；pos-删除位置（1<=pos<=length）；data-输出参数（存删除数据，可为NULL）
// 返回：成功true，失败false（pos非法/空表）
bool Linklist_DeletePos(Linklist* L, int pos, ElemType* data);

// 11. 按值删除所有匹配节点（不带头节点）
// 参数：L-头指针的指针；val-目标值
// 返回：成功true（至少删除1个），失败false（无匹配值/空表）
bool Linklist_DeleteVal(Linklist* L, ElemType val);

// 12. 链表反转（不带头节点，返回新头指针）
// 参数：L-原链表头指针
// 返回：反转后的新头指针（空表返回NULL）
Linklist Linklist_Reverse(Linklist L);

// 13. 合并两个有序链表（升序合并，不带头节点，原链表不改变）
// 参数：L1-第一个有序链表头指针；L2-第二个有序链表头指针
// 返回：合并后的新有序链表头指针
Linklist Linklist_Merge(Linklist L1, Linklist L2);

// 14. 查找链表中间节点（不带头节点）
// 参数：L-链表头指针
// 返回：中间节点指针（空表返回NULL）
LNode* Linklist_FindMid(Linklist L);

// 15. 查找链表倒数第k个节点（不带头节点）
// 参数：L-链表头指针；k-倒数第k个（k>=1）
// 返回：目标节点指针（k越界/空表返回NULL）
LNode* Linklist_FindKthFromEnd(Linklist L, int k);

// 16. 判断链表是否有环（不带头节点）
// 参数：L-链表头指针
// 返回：有环true，无环false
bool Linklist_HasCycle(Linklist L);

// 17. 查找链表环的入口节点（不带头节点，无环返回NULL）
// 参数：L-链表头指针
// 返回：环入口节点指针（无环/空表返回NULL）
LNode* Linklist_FindCycleEntry(Linklist L);

// 18. 打印链表（不带头节点，空格分隔数据）
// 参数：L-链表头指针
// 返回：成功true（非空表），失败false（空表/参数NULL）
bool Linklist_Print(Linklist L);

// 19. 销毁链表（不带头节点，释放所有节点，头指针置NULL）
// 参数：L-头指针的指针
void Linklist_Destroy(Linklist* L);

#endif // LINKLIST_H