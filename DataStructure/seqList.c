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

void Seqlist_test(){
    Seqlist L;
    ElemType del_val, get_val;
    int* pos_arr = NULL;

    // ===================== Step 1: 初始化测试 =====================
    printf("===== Step 1: Init Seqlist =====\n");
    if (!Seqlist_Init(&L)) {
        printf("Init Seqlist failed!\n");
        return -1;
    }
    printf("Init success: Maxsize=%d, length=%d\n", L.Maxsize, L.length);
    Seqlist_Print(&L); // 空表

    // ===================== Step 2: 插入测试 =====================
    printf("\n===== Step 2: Test Insert =====\n");
    Seqlist_Insert(&L, 1, 10);    // 合法位置（pos=1）
    Seqlist_Insert(&L, 2, 20);    // 合法位置（pos=2）
    Seqlist_Insert(&L, 5, 30);    // 越界，自动修正为length+1=3
    Seqlist_Insert(&L, 0, 40);    // 非法位置（pos<1）
    printf("After insert: length=%d\n", L.length);
    Seqlist_Print(&L); // 预期：pos1=10, pos2=20, pos3=30

    // ===================== Step 3: 按位置删除测试 =====================
    printf("\n===== Step 3: Test Delete by Pos =====\n");
    Seqlist_DeletePos(&L, 2, &del_val);  // 合法位置（pos=2）
    Seqlist_DeletePos(&L, 10, &del_val); // 越界，自动修正为最后一位
    Seqlist_DeletePos(&L, 0, &del_val);  // 非法位置（pos<1）
    Seqlist_DeletePos(&L, 1, NULL);      // 不传返回值
    printf("After delete by pos: length=%d\n", L.length);
    Seqlist_Print(&L); // 空表

    // ===================== Step 4: 按值删除测试 =====================
    printf("\n===== Step 4: Test Delete by Val =====\n");
    // 重新插入：10,20,10,30,10
    Seqlist_Insert(&L, 1, 10);
    Seqlist_Insert(&L, 2, 20);
    Seqlist_Insert(&L, 3, 10);
    Seqlist_Insert(&L, 4, 30);
    Seqlist_Insert(&L, 5, 10);
    printf("Before delete by val: ");
    Seqlist_Print(&L); // 10,20,10,30,10

    Seqlist_DeleteVal(&L, 10);    // 删除所有10（预期剩余20,30）
    printf("After delete val=10: length=%d\n", L.length);
    Seqlist_Print(&L);

    Seqlist_DeleteVal(&L, 99);    // 删除不存在的值
    // 插入全为5的元素
    Seqlist_Insert(&L, 1, 5);
    Seqlist_Insert(&L, 2, 5);
    Seqlist_Insert(&L, 3, 5);
    printf("Before delete all val=5: ");
    Seqlist_Print(&L); // 20,30,5,5,5
    Seqlist_DeleteVal(&L, 5);     // 删除所有5
    printf("After delete all val=5: length=%d\n", L.length);
    Seqlist_Print(&L); // 20,30

    // ===================== Step 5: 空表删除测试 =====================
    printf("\n===== Step 5: Test Delete on Empty List =====\n");
    // 清空顺序表
    while (L.length > 0) {
        Seqlist_DeletePos(&L, 1, &del_val);
    }
    Seqlist_DeletePos(&L, 1, &del_val);  // 空表按位置删除
    Seqlist_DeleteVal(&L, 10);           // 空表按值删除

    // ===================== Step 6: 按位置取值测试 =====================
    printf("\n===== Step 6: Test GetPos =====\n");
    // 重新初始化并插入数据
    Seqlist_Init(&L);
    Seqlist_Insert(&L, 1, 10);
    Seqlist_Insert(&L, 2, 20);
    Seqlist_Insert(&L, 3, 10);
    Seqlist_Insert(&L, 4, 30);
    Seqlist_Insert(&L, 5, 10);
    printf("Init Seqlist for Get test: ");
    Seqlist_Print(&L);

    Seqlist_GetPos(&L, 3, &get_val);  // 合法位置（pos3=10）
    Seqlist_GetPos(&L, 0, &get_val);  // 非法位置（pos<1）
    Seqlist_GetPos(&L, 10, &get_val); // 越界，自动修正为最后一位

    // ===================== Step 7: 按值找位置测试 =====================
    printf("\n===== Step 7: Test GetVal =====\n");
    pos_arr = Seqlist_GetVal(&L, 10); // 存在（pos1,3,5）
    if (pos_arr != NULL) {
        printf("Returned pos array: ");
        for (int i = 0; i < 3; i++) { // 已知匹配数为3
            printf("%d ", pos_arr[i]);
        }
        printf("\n");
        free(pos_arr); // 释放动态数组
        pos_arr = NULL;
    }
    Seqlist_GetVal(&L, 99); // 不存在的值

    // ===================== Step 8: 边界测试（空表/NULL指针） =====================
    printf("\n===== Step 8: Boundary Test =====\n");
    L.length = 0; // 清空
    Seqlist_GetPos(&L, 1, &get_val);  // 空表GetPos
    Seqlist_GetVal(&L, 10);           // 空表GetVal
    Seqlist_GetPos(NULL, 1, &get_val); // NULL指针GetPos
    Seqlist_GetVal(NULL, 10);          // NULL指针GetVal

    // ===================== Step 9: 销毁测试 =====================
    printf("\n===== Step 9: Test Drop =====\n");
    Seqlist_Drop(&L);
    Seqlist_Print(&L); // 已销毁，data为NULL

    printf("\n===== All Test Finished =====\n");
    return 0;
}
