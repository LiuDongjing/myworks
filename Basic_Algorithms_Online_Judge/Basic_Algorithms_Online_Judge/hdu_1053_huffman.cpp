#include <iostream>
#include <vector>
using namespace std;
class Node {
public:
	int count = 0;
	int value= -1;
	Node *left = nullptr;
	Node *right = nullptr;
	Node *next = nullptr;
};
int main() {
	string str;
	while (scanf("%s", &str) > 0) {
		if (str == "END") {
			break;
		}
		vector<int> data(31, 0);//第31个是下划线
		for (int i = 0; i < str.size(); i++) {
			if (str[i] != '_')
				data[str[i] - 'A']++;
		}
		Node *head = nullptr;
		for (int i = 0; i < data.size(); i++) {
			if (data[i] > 0) {
				Node *t = new Node();
				t->value = i;
				t->count = data[i];
				if (head == nullptr) {
					head = t;
					continue;
				}

			}
		}
	}
	return 0;
}