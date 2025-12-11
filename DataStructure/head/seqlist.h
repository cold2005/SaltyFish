#ifndef SEQLIST_H
#define SEQLIST_H

#include"common.h"  // 包含ElemType、bool等定义

// 顺序表（动态数组）结构体
typedef struct{
    ElemType* data;   // 存储数据的动态数组指针
    int length;       // 当前顺序表中有效元素个数（初始为0）
    int Maxsize;      // 顺序表最大容量（动态扩容时使用）
}Seqlist;

// 1. 初始化顺序表（分配初始内存，初始化长度和最大容量）
// 参数：L-顺序表指针（需修改结构体成员）
// 返回：成功true，失败false（内存分配失败/参数NULL）
bool Seqlist_Init(Seqlist* L);

// 2. 按位置插入元素（pos从1开始，插入到pos位置）
// 参数：L-顺序表指针；pos-插入位置（1<=pos<=length+1）；data-待插入元素
// 返回：成功true，失败false（pos非法/容量已满/参数NULL）
bool Seqlist_Insert(Seqlist* L, int pos, ElemType data);

// 3. 按位置删除元素（pos从1开始）
// 参数：L-顺序表指针；pos-删除位置（1<=pos<=length）；val-输出参数（存储删除元素，可为NULL）
// 返回：成功true，失败false（pos非法/表空/参数NULL）
bool Seqlist_DeletePos(Seqlist* L, int pos, ElemType* val);

// 4. 按值删除所有匹配元素
// 参数：L-顺序表指针；val-待删除目标值
// 返回：成功true（至少删除1个），失败false（无匹配值/表空/参数NULL）
bool Seqlist_DeleteVal(Seqlist* L, ElemType val);

// 5. 按位置取值（pos从1开始）
// 参数：L-顺序表指针；pos-目标位置（1<=pos<=length）；value-输出参数（存储取值结果，不可为NULL）
// 返回：成功true，失败false（pos非法/表空/参数NULL）
bool Seqlist_GetPos(Seqlist* L, int pos, ElemType* value);

// 6. 按值查找（返回所有匹配元素的位置数组，位置从1开始）
// 参数：L-顺序表指针；val-目标值
// 返回：成功返回位置数组（末尾以-1标识结束），失败返回NULL（无匹配值/表空/参数NULL）
int* Seqlist_GetVal(Seqlist* L, ElemType val);

// 7. 打印顺序表（输出所有有效元素，空格分隔）
// 参数：L-顺序表指针（非NULL）
void Seqlist_Print(Seqlist* L);

// 8. 销毁顺序表（释放动态数组内存，重置成员）
// 参数：L-顺序表指针（需置空data，length和Maxsize归0）
void Seqlist_Drop(Seqlist* L);

// 9. 顺序表功能测试（含初始化、插入、删除、打印、销毁等流程）
void Seqlist_test();

#endif // SEQLIST_H