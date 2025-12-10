#ifndef SEQLIST_H
#define SEQLIST_H

#include"common.h"

typedef struct{
    ElemType* data;
    int length;
    int Maxsize;
}Seqlist;

bool Seqlist_Init(Seqlist*L);

bool Seqlist_Insert(Seqlist*L,int pos,ElemType data);

bool Seqlist_DeletePos(Seqlist*L,int pos,ElemType* val);

bool Seqlist_DeleteVal(Seqlist*L,ElemType val);

bool Seqlist_GetPos(Seqlist*L,int pos,ElemType* value);

int* Seqlist_GetVal(Seqlist* L,ElemType*val);

void Seqlist_Print(Seqlist* L);

void Seqlist_Drop(Seqlist* L);

void Seqlist_test();

#endif