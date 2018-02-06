#include <iostream>
#include <queue>
#include <vector>
using namespace std;
class Node {
public:
	int index;
	int incount;
	Node() {
		index = 0;
		incount = 0;
	}
	bool operator <(const Node&other)const {
		return index > other.index;
	}
};
int main() {
#ifdef _DEBUG
	freopen("hdu_1285_topological_sorting.txt", "r", stdin);
#endif
	int n, m;
	while (0 < scanf("%d%d", &n, &m)) {
		vector<vector<bool> > mat(n + 1, vector<bool>(n + 1, false));
		vector<Node> flag(n + 1);
		for (int i = 1; i <= n; i++) {
			flag[i].index = i;
		}
		for (int i = 0; i < m; i++) {
			int a, b;
			scanf("%d%d", &a, &b);
			// 关键，有重复的数据。
			if (mat[a][b]) continue;
			mat[a][b] = true;
			flag[b].incount++;
		}
		priority_queue<Node> que;
		for (int i = 1; i <= n; i++) {
			if (flag[i].incount == 0) {
				que.push(flag[i]);
			}
		}
		bool f = true;
		while (!que.empty()) {
			Node t = que.top();
			que.pop();
			if (f) {
				f = false;
				printf("%d", t.index);
			}
			else {
				printf(" %d", t.index);
			}
			for (int i = 1; i <= n; i++) {
				if (mat[t.index][i]) {
					flag[i].incount--;
					mat[t.index][i] = false;
					if (flag[i].incount == 0) {
						que.push(flag[i]);
					}
				}
			}
		}
		printf("\n");
	}
	return 0;
}