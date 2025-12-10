#ifndef SEQLIST.h
#define SEQLIST.h

#include"common.h"

typedef struct{
    ElemType* data;
    int length;
    int Maxsize;
}Seqlist;

bool Initlist(Seqlist*L);

bool InsertData(Seqlist*L,int pos,int data);

bool DeleteDataPos(Seqlist*L,int pos);

bool DeleteDataVal(Seqlist*L,int val);

void SearchBypos(Seqlist*L,int pos);

void SearchByval(Seqlist* L,int val);

bool ChangeDataByPos(Seqlist* L,int newdata,int pos);

bool ChangeDataByVal(Seqlist*L , int newdata, int val);

void Printlist(Seqlist* L);



#endif