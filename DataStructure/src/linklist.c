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
    printf("Success:Linklist_CreatNode\n");
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
        printf("Success(Linklist_InsertPos):InsertPos is [%d].\n",pos);
        return true;
    }
   
    ElemType val;
    LNode* previous = Linklist_GetPos((*L),pos-1,&val);
    if(previous==NULL) return false;

    newnode->next = previous->next;
    previous->next = newnode;
    printf("Success(Linklist_InsertPos):InsertPos is [%d]].\n",pos);
    return true;
}

bool Linklist_InsertHead(Linklist* L, ElemType data){
    if (L==NULL){
        return false;
    }
    LNode* newnode = Linklist_CreatNode(data);
    if(newnode==NULL){
        return false;
    }
    newnode->next = (*L);
    (*L) = newnode;
    printf("Success(Linklist_InsertHead):insert the data to the head.\n");
    return true;
}

bool Linklist_InsertTail(Linklist* L, ElemType data){
    if(L==NULL){
        printf("Error:The Linklist* is nullptr plase check.\n");
        return false;
    }
    LNode* newnode = Linklist_CreatNode(data);
    if(newnode == NULL){
        return false;
    }
    LNode* pos = (*L);
    if(pos == NULL){
        (*L) = newnode;
        printf("Success(Linklist_InsertTail):insert the data to the end.\n");
        return true;
    }
    while(pos->next!=NULL){
        pos = pos->next;
    }
    pos->next = newnode;
    printf("Success(Linklist_InsertTail):insert the data to the end.\n");
    return true;
}

bool Linklist_DeletePos(Linklist* L, int pos, ElemType* data){
    if(L==NULL){
        printf("Error:The Linklist* is nullptr.\n");
        return false;
    }
    if(pos<1){
        printf("Error(Linklist_DeletePos):The pos is illegal.\n");
        return false;
    }

    if(*L==NULL){
        printf("Error(Linklist_DeletePos):This Linklist is empty so that can't delete data.\n");
        return false;
    }
    if(pos==1){
        LNode* temp = (*L);
        (*L) = (*L)->next;
        free(temp);
        printf("Success(Linklist_DeletePos):Delete and free the first node.\n");
        return true;
    }

    LNode* previous = Linklist_GetPos((*L),pos-1,data);

    if(previous == NULL||previous->next==NULL) return false;
    LNode* temp = previous->next;
    *data = temp->data;
    previous->next = temp->next;
    free(temp);
    printf("Success(Linklist_DeletePos):Delete and free the Element which pos is %d\n",pos);
    return true;
}

bool Linklist_DeleteVal(Linklist* L, ElemType val){
    if(L==NULL){
        printf("Error:The Linklist* is nullptr please check.\n");
        return false;
    }
    if((*L)==NULL){
        printf("Error(Linklist_DeleteVal):The Linklist is Empty can't delete.\n");
        return false;
    }
    LNode* pos = (*L);
    int count = 0;
    while(pos->next!=NULL){
        if(pos->next->data==val){
            LNode* temp = pos->next;
            pos->next = temp->next;
            free(temp);
            count++;
        }
       else{pos = pos->next;}
    }
    if((*L)->data == val){
        LNode* temp = (*L);
        (*L) = (*L)->next;
        free(temp);
        count++;
    }
    printf("Success(Linklist_DeleteVal):Delete Finish [%d]\n ",count);
    return true;
}

Linklist Linklist_Reverse(Linklist L){
    if(L==NULL){
        printf("Error:Can't reverse this list because it is empty.\n");
        return NULL;
    }
    
    
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

