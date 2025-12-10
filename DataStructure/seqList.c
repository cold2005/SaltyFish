#include"seqlist.h"

bool Seqlist_Init(Seqlist*L){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return false;
    }
    L->data = (ElemType*)malloc(sizeof(ElemType)*InitSize);
    if((L->data)==NULL){
        printf("Error:Initlist\n");
        return false;
    }
    L->Maxsize = InitSize;
    L->length = 0;
    return true;
}

bool Seqlist_Insert(Seqlist*L,int pos,int data){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return false;
    }
    if(L->length>=L->Maxsize){
        printf("Error:Seqlist is full.\n");
        return false;
    }
    if(pos < 1){
        printf("Error:Seqlist insert pos is illegal.\n");
        return false;
    }
    if(pos>L->length){
        printf("Warning:Pos is over this Seqlist,Now change pos is LastPos %d\n",L->length);
        pos = L->length;
    }
    for(int i = L->length; i > pos - 1 ; i--){
        L->data[i] = L->data[i-1];
    }
    L->data[pos - 1 ] = data;
    L->length++;
    printf("Success to insert.\n");
    return true;
}

bool Seqlist_DeletePos(Seqlist*L,int pos,ElemType* val){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return false;
    }
    if(L->length == 0){
        printf("Error:Seqlist is an empty list.\n");
        return false;
    }
   
    if(pos < 1){
        printf("Error:Seqlist delete pos is illegal.\n");
        return false;
    }

     if(pos>L->length){
        printf("Warning:Pos is over this Seqlist,Now change pos to LastPos %d\n",L->length);
        pos = L->length;
    }

    if(val != NULL){
         (*val) = L->data[pos - 1];
    }
    else{
        printf("Warning:Seqlist delete function can't return value,the val is nullptr.\n");
    }
    for(int i = pos;i < L->length;i++){
        L->data[i-1] = L->data[i];
    }
    L->length--;
    if (val != NULL) {
        printf("Success to delete pos:%d, value:%d.\n", pos, *val);
    } else {
        printf("Success to delete pos:%d (no return value).\n", pos);
    }
    return true;
}

bool Seqlist_DeleteVal(Seqlist*L,ElemType val){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return false;
    }
    if(L->length == 0){
        printf("Error:Seqlist is an empty List.\n");
        return false;
    }
    int count = 0;
    for(int i = 0;i<L->length;i++){
        if(L->data[i] != val){
            L->data[count] = L->data[i];
            count++;
        }
    }

    if(count == L->length){
        printf("Error:No this value in Seqlist.\n");
        return false;
    }
    L->length = count;
    if(count == 0){
        printf("Success to delete.(All data are value!All Delete)\n");
        L->length = 0;
        return true;
    }
    printf("Success to delete,now this Seqlist has %d data \n",count);
    return true;
}

void Seqlist_Print(Seqlist* L){
    if(L==NULL){
         printf("Error:Seqlist is nullptr.\n");
         return;
    }
    if(L->length == 0){
        printf("Error:Seqlist is an empty list.\n");
        return;
    }
    for(int i = 0;i<L->length;i++){
        printf("pos[%d] data is [%d]\n",i,L->data[i]);
    }
    return;
}