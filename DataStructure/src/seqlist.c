#include"../head/seqlist.h"

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

bool Seqlist_Insert(Seqlist*L,int pos,ElemType data){
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
    if(pos > L->length + 1){
        printf("Warning:Pos is over this Seqlist,Now change pos is LastPos %d\n",L->length+1);
        pos = L->length + 1;
    }
    //将 pos > L->length 修改为 pos > length + 1 时才合理 我们应该允许插入值到顺序表末尾
    //否则 当初始时 顺序表长度为零 往位置1 插入数据 就会被判定为不合法 明显不符合常理
    for(int i = L->length; i > pos - 1 ; i--){
        L->data[i] = L->data[i-1];
    }
    L->data[pos - 1] = data;
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
        return true;
    }
    printf("Success to delete,now this Seqlist has %d data \n",count);
    return true;
}

bool Seqlist_GetPos(Seqlist*L,int pos,int* value){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return false;
    }
    if(L->length == 0){
        printf("Error:Seqlist is an empty list.\n");
        return false;
    }
   
    if(pos < 1){
        printf("Error:Seqlist get pos is illegal.\n");
        return false;
    }

     if(pos>L->length){
        printf("Warning:Pos is over this Seqlist,Now change pos to LastPos %d\n",L->length);
        pos = L->length;
    }
    printf("Success:The value of pos:%d is %d\n",pos,L->data[pos - 1]);
    (*value) = L->data[pos - 1];
    return true;
}

int* Seqlist_GetVal(Seqlist* L,int val){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return NULL;
    }
    if(L->length == 0){
        printf("Error:Seqlist is an empty list.\n");
        return NULL;
    }
    int count = 0;
    

    for(int i = 0;i <L->length;i++){
        if(L->data[i] == val){
            count++;
        }
    } 

    if(count==0){
        printf("Error:No this val in this Seqlist.\n");
        return NULL;
    }
    int* arr = (int*)malloc(sizeof(int)*count);

    if(arr==NULL){
        printf("Error:Crear arr Wrong! Can\'t return pos array\n");
        return NULL;
    }
    count = 0;
    for(int i = 0;i <L->length;i++){
        if(L->data[i] == val){
            arr[count] = i+1;
            count++;
        }
    } 
    printf("Success: %d positions found for value %d (returned array, pos start from 1).\n",count,val);
    return arr;
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
        printf("pos[%d] data is [%d]\n",i+1,L->data[i]);
    }
    return;
}

void Seqlist_Drop(Seqlist* L){
    if(L==NULL){
        printf("Error:Seqlist is nullptr.\n");
        return;
    }
    if(L->data == NULL){
        printf("No need to Drop.\n");
        return;
    }
    free(L->data);
    L->data =NULL;
    L->length = 0;
    return;
}
