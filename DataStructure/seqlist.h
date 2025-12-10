#ifndef SEQLIST.h
#define SEQLIST.h

#include"common.h"

typedef struct{
    ElemType* data;
    int length;
    int Maxsize;
}Seqlist;

bool Seqlist_Initlist(Seqlist*L);

bool Seqlist_InsertData(Seqlist*L,int pos,int data);

bool Seqlist_DeleteDataPos(Seqlist*L,int pos);

bool Seqlist_DeleteDataVal(Seqlist*L,int val);

void Seqlist_SearchBypos(Seqlist*L,int pos);

void Seqlist_SearchByval(Seqlist* L,int val);

bool Seqlist_ChangeDataByPos(Seqlist* L,int newdata,int pos);

bool Seqlist_ChangeDataByVal(Seqlist*L , int newdata, int val);

void Seqlist_Printlist(Seqlist* L);

void Seqlist_DropList(Seqlist* L);


#endif