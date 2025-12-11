#include"../head/linklist.h"

bool Linklist_Init(Linklist* L){
    if(L==NULL){
        printf("Error:nullptr.\n");
        return false;
    }
    *L = NULL;
    printf("Success:Linklist_Init.\n");
    return true;
}

LNode* Linklist_CreatNode(ElemType data){
    LNode* node = (LNode*)malloc(sizeof(LNode));
    if(node==NULL){
        printf("Error:Assgin memory wrong.\n");
        return NULL;
    }
    node ->data = data;
    node ->next = NULL;
    printf("Success:Linklist_CreatNode,data is %d\n",node->data);
    return node;
}

bool Linklist_IsEmpty(Linklist L){
    if(L==NULL){
        printf("This Linklist is Empty.\n");
        return true;
    }
    else{
        printf("This Linklist is not Empty!\n");
        return false;
    }
}

int Linklist_Length(Linklist L){
    if(L==NULL){
        return 0;
    }
    int length = 0;
    LNode* pos = L;
    while(pos!=NULL){
        pos = pos->next;
        length++;
    }
    return length;
}

LNode* Linklist_GetPos(Linklist L, int pos, ElemType* data){
    if(L==NULL){
        printf("Warning(Linklist_GetPos):The Linklist is nullptr\n");
        return NULL;
    }
    if(data == NULL){
       printf("Warning(Linklist_GetPos):The data is nullptr please check parameter.\n");
       return NULL;
    }
    if(pos < 1) {
        printf("Warning(Linklist_GetPos):The pos is illegal\n");
        return NULL;}
    LNode* temp = L;
    for(int i = 0;i < pos-1 &&temp != NULL;i++){
        temp = temp->next;
    }
    if(temp==NULL) {
        printf("Warning(Linklist_GetPos):The pos is illegal\n");
        return NULL;
    }
    *data = temp -> data;
    return temp;
}

LNode* Linklist_GetVal(Linklist L, ElemType val){
    if(L==NULL){
        printf("Waring(Linklist_GetVal):The Linklist is nullpter\n");
        return NULL;
    }
    LNode* temp = L;
    while(temp!=NULL&&temp->data != val){
        temp = temp->next;
    }
    if(temp == NULL){
        printf("Error(Linklist_GetVal):Can't find the element which value is %d in this Linklist.\n",val);
        return NULL;
    }
    else{
        printf("Success(Linklist_GetVal):Get the frist element which value is %d.\n",val);
        return temp;
    }
}

bool Linklist_InsertPos(Linklist* L, int pos, ElemType data){
    if(L==NULL){
        printf("Error:The Linklist* is nullptr plase check.\n");
        return false;
    }
    int length = Linklist_Length((*L));
    if(pos < 1){
        printf("Error(Linklist_InsertPos):The pos is illegal.\n");
        return false;
    }
    if(pos > length+1){
        printf("Waring(Linklist_InsertPos):The pos over this Linklist,now change it to %d",length + 1);
        pos = length+1;
    }

    LNode* newnode = Linklist_CreatNode(data);
    if(newnode == NULL) return false;

    if(pos==1){
        newnode->next = (*L);
        (*L) = newnode;
        printf("Success(Linklist_InsertPos):InsertPos is [%d],InsertData is [%d].\n",pos,data);
        return true;
    }
   
    ElemType val;
    LNode* previous = Linklist_GetPos((*L),pos-1,&val);
    if(previous==NULL) return false;

    newnode->next = previous->next;
    previous->next = newnode;
    printf("Success(Linklist_InsertPos):InsertPos is [%d],InsertData is [%d].\n",pos,data);
    return true;
}

bool Linklist_InsertHead(Linklist* L, ElemType data){
    
}

int main(void){
    Linklist L = NULL;
    Linklist_IsEmpty(L);
    Linklist_Init(&L);
    Linklist_IsEmpty(L);
    Linklist_InsertPos(&L,1,10);
    Linklist_InsertPos(&L,2,20);
    Linklist_InsertPos(&L,3,30);
    Linklist_InsertPos(&L,-1,1);
    printf("\n\n\n");
    ElemType data;
    Linklist_GetPos(L,0,&data);
    Linklist_GetPos(L,1,&data);
    Linklist_GetPos(L,2,NULL);
    Linklist_GetPos(L,10,&data);
    printf("\n\n\n");
    Linklist_GetVal(L,20);
}

