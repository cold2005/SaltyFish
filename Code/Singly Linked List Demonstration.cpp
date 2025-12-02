#include<iostream>

typedef struct Node{
    int data;
    struct Node* next;
}LNode,*LinkList;

bool InitList(LinkList& L){

    L = (LNode*)malloc(sizeof(LNode));
    if(L==NULL) return false;
    L->next = NULL;
    return true;

}

LNode* CreatLNode(int data){

    LNode* node = (LNode*)malloc(sizeof(LNode));
    if(node == NULL){
        printf("Error to assign mermory.");
        return NULL;
    }
    node->next = NULL;
    node->data = data;
    return node;
}

bool DropList(LinkList& L){
    if(L==NULL){
        return false;
    }
    LNode* pos = L->next;
    LNode* ptr = NULL;
    while(pos!=NULL){
        ptr = pos ->next;
        free(pos);
        pos = ptr;
    }
    free(L);
    L = NULL;
    return true;
}

LNode* GetLNodeByPos(LinkList L,int pos,int& data){

    if(L==NULL){
        printf("NO list.\n");
        return NULL;
    }

    if(pos==0){
        return L;
    } 

    if(pos<0){
        printf("Wrong Pos.\n");
        return NULL;
    }

    LNode* ptr = L->next;

    for(int i = 0;i < pos - 1 && ptr != NULL;i++){
        ptr = ptr->next;
    }

    if(ptr == NULL){
        printf("Pos Over this List.\n");
        return NULL;
    }

    data = ptr->data;

    return ptr;
}


bool InsertNextLNode(LNode* target,LNode* newLNode){

    if(target == NULL || newLNode == NULL){
        printf("There is a NULL ptr in this Two Nodes.\n");
        return false;
    }
    newLNode ->next = target ->next;
    target->next = newLNode;
    printf("插入成功！\n");
    return true;
}

bool DeleteNowLNode(LNode* target){
    if(target == NULL) return false;
    if(target -> next==NULL){
        printf("You Should Know The List To Delete This LNode.\n"); 
        return false;   
    }
    target->data = target->next->data;
    LNode* temp = target->next;
    target->next = target->next->next;
    free(temp);
    return true;
}

bool InsertLNode(LinkList& L,int pos,int data){
    int pervious = 0;
    LNode* pLNode = GetLNodeByPos(L,pos-1,pervious);
    LNode* NewLNode = CreatLNode(data);
    if(NewLNode == NULL) return false;
    return InsertNextLNode(pLNode,NewLNode);
}

bool DeleteLNode(LinkList& L,int pos){
    int data = 0;
    LNode* p = GetLNodeByPos(L,pos-1,data);
    if(p==NULL){
        printf("Wrong Pos or NULL LinkList.\n");
        return false;
    }
    if(p->next == NULL){
        printf("Wrong Pos Over the LinkList.\n");
        return false;
    }
    LNode* temp = p->next;

    p->next = p->next->next;

    free(temp);

    return true;

}

bool ChangeLNode(LinkList& L,int pos,int value){
    int data = 0;
    if(pos == 0){
        printf("You can't change head LNode.\n");
        return false;
    }
    LNode* p = GetLNodeByPos(L,pos,data);
    if(p==NULL) return false;
    p->data = value;
    return true;
}

bool Print(LinkList L){
    if(L==NULL) return false;
    LNode* ptr = L->next;
    int index = 1;
    while(ptr!=NULL){
        printf("第%d个数据是%d. \n",index,ptr->data);
        index++;
        ptr = ptr->next;
    }
    printf("--------------------------\n");

    return true;
}

bool SearchByPos(LinkList L,int pos){
    int data = 0;
    if(pos == 0){
        printf("你不能查找头结点的值 因为头结点不带有数据。\n");
        return false;
    }
    if(GetLNodeByPos(L,pos,data)!=NULL){
        printf("你所查找的第%d个位置的数据为%d .\n",pos,data);
        return true;
    }
    else{
        return false;
    }

}
int main(void){
    LinkList L;

    if(!InitList(L)){
        printf("初始化失败！ 程序退出！\n");
        return 0;
    }

    printf("请输入链表数据 输入非数字时 终止输入。\n");

    int data = 0;
    LNode* temp = L;
    LNode* newLNode = NULL; 
    while(scanf("%d",&data)){
        newLNode = CreatLNode(data);
        if(newLNode == NULL){
            break;
        }
        InsertNextLNode(temp,newLNode);
        temp = newLNode;
        
    }

    Print(L);
    
    SearchByPos(L,4);

    InsertLNode(L,3,102);

    Print(L);

    DeleteLNode(L,3);

    Print(L);

    DropList(L);

    return 0;

}