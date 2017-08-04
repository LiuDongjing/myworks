#include <iostream>
#include <vector>
using namespace std;
class Node {
public:
	Node(int c, int v=-1) {
		count = c;
		value = v;
	}
	int count = 0;
	int value= -1;
	Node *left = nullptr;
	Node *right = nullptr;
};
class ListNode {
public:
	ListNode(Node * v){
		value = v;
	}
	Node *value = nullptr;
	ListNode *next = nullptr;
};
//从小到大排序
void insertion_sort(ListNode* &head, Node *v) {
	if (v == nullptr) return;
	ListNode* t = new ListNode(v);
	if (head == nullptr) {
		head = t;
		return;
	}
	if (head->value->value > v->value) {
		t->next = head;
		head = t;
		return;
	}
	ListNode *prev = head, *next = head->next;
	for (; next != nullptr; prev=prev->next, next=next->next) {
		if (next->value->value > v->value) {
			t->next = next;
			prev->next = t;
			return;
		}
	}
	prev->next = t;
}
int main() {
	string str;
	while (scanf("%s", &str) > 0) {
		if (str == "END") {
			break;
		}
		vector<int> data(31, 0);//第31个是下划线
		for (int i = 0; i < str.size(); i++) {
			data[str[i] - 'A']++;
		}
		ListNode *head = nullptr;
		for (int i = 0; i < data.size(); i++) {
			if (data[i] > 0) {
				Node *t = new Node(data[i], i);
				insertion_sort(head, t);
			}
		}
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
			throw runtime_error("链表头为空!");
		}
		Node *huffman = head->value;
	}
	return 0;
}