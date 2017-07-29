#include <iostream>
#include <vector>
using namespace std;
class Node {
public:
	Node *left = nullptr;
	Node *right = nullptr;
	int value = 0;
};
Node * build_tree(vector<int> &pre, vector<int> &in,
	int pre_start, int in_start, int len) {
	if (len <= 0) return nullptr;
	Node *h = new Node();
	h->value = pre[pre_start];
	int s = 0;
	for (; s < len && in[in_start+s] != pre[pre_start]; s++);
	h->left = build_tree(pre, in, pre_start + 1, in_start, s);
	h->right = build_tree(pre, in, pre_start + s + 1, in_start + s + 1, len - s - 1);
	return h;
}
void post_order(Node *h, Node *head) {
	if (h == nullptr) {
		return;
	}
	post_order(h->left, head);
	post_order(h->right, head);
	printf("%d", h->value);
	if (h != head) printf(" ");
	else printf("\n");
	delete h;
}
int main() {
#ifdef _DEBUG
	freopen("hdu_binary_tree_traverals.txt", "r", stdin);
#endif
	int n;
	while (scanf("%d", &n) > 0) {
		vector<int> preorder(n);
		vector<int> inorder(n);
		for (int i = 0; i < n; i++)
			scanf("%d", &preorder[i]);
		for (int i = 0; i < n; i++)
			scanf("%d", &inorder[i]);
		Node *head = build_tree(preorder, inorder, 0, 0, n);
		post_order(head, head);
	}
	return 0;
}