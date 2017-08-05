#include <iostream>
#include <vector>
#include <exception>
using namespace std;
//huffman���ڵ�
class Node {
public:
	Node(int c, int v=-1) {
		count = c;
		value = v;
	}
	int count = 0;//�ַ���Ƶ��
	int value= -1;//�ַ�����
	Node *left = nullptr;
	Node *right = nullptr;
};
//������������ڵ�
class ListNode {
public:
	ListNode(Node * v){
		value = v;
	}
	Node *value = nullptr;
	ListNode *next = nullptr;
};
//��count��С��������
void insertion_sort(ListNode* &head, Node *v) {
	if (v == nullptr) return;
	ListNode* t = new ListNode(v);
	if (head == nullptr) {
		head = t;
		return;
	}
	if (head->value->count > v->count) {
		t->next = head;
		head = t;
		return;
	}
	ListNode *prev = head, *next = head->next;
	for (; next != nullptr; prev=prev->next, next=next->next) {
		if (next->value->count > v->count) {
			t->next = next;
			prev->next = t;
			return;
		}
	}
	prev->next = t;
}
// ͳ��huffman������Ҫ��bit��
void sum_bits(const Node* head, int &sum, int height = 0) {
	if (head == nullptr) return;
	if (head->left == nullptr && head->right == nullptr) {
		sum += height*head->count;
		return;
	}
	if (head->left != nullptr) sum_bits(head->left, sum, height + 1);
	if (head->right != nullptr) sum_bits(head->right, sum, height + 1);
}
int main() {
#ifdef _DEBUG
	freopen("hdu_1053_huffman.txt", "r", stdin);
#endif
	char buf[1024];
	while (scanf("%s", buf) > 0) {
		string str = buf;
		if (str == "END") {
			break;
		}
		vector<int> data(31, 0);//��31�����»���
		for (int i = 0; i < str.size(); i++) {
			data[str[i] - 'A']++;
		}
		//��ʼ�����б���С��������
		ListNode *head = nullptr;
		for (int i = 0; i < data.size(); i++) {
			if (data[i] > 0) {
				Node *t = new Node(data[i], i);
				insertion_sort(head, t);
			}
		}
		//�ϲ���
		while (head != nullptr && head->next != nullptr) {
			Node *n1 = head->value;
			Node *n2 = head->next->value;
			Node *n = new Node(n1->count + n2->count);
			n->left = n1;
			n->right = n2;
			ListNode *tmp = head->next;
			delete head;
			head = tmp->next;
			delete tmp;
			insertion_sort(head, n);
		}
		if (head == nullptr) {
			throw runtime_error("����ͷΪ��!");
		}
		Node *huffman = head->value;
		int sum = 0;
		sum_bits(huffman, sum);
		printf("%d %d %.1f\n", 8*str.size(), sum, 8*str.size() / float(sum));
	}
	return 0;
}