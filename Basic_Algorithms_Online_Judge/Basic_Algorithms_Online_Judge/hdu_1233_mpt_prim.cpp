#include <iostream>
#include <vector>
#include <queue>
using namespace std;
class Edge {
public:
	int node;
	int weight;
	Edge(int n, int w) {
		node = n;
		weight = w;
	}
	bool operator < (const Edge &other) const {
		return weight > other.weight;
	}
};

int main() {
	int n;
#ifdef _DEBUG
	freopen("hdu_1233_minimum_spanning_tree.txt", "r", stdin);
#endif
	while (scanf("%d", &n) > 0) {
		if (n == 0) break;
		vector<bool> mark(n + 1, true);
		vector<vector<int> > mat(n + 1, vector<int>(n + 1, 0));
		for (int i = 0; i < n*(n - 1) / 2; i++) {
			int a, b, w;
			scanf("%d%d%d", &a, &b, &w);
			mat[a][b] = w;
			mat[b][a] = w;
		}
		int c = 1, node = 1, d = 0;
		priority_queue<Edge> que;
		while (c < n) {
			mark[node] = false;
			for (int i = 1; i <= n; i++) {
				if (mat[node][i] > 0 && mark[i]) {
					que.push(Edge(i, mat[node][i]));
				}
			}
			while (!que.empty()) {
				Edge t = que.top();
				que.pop();
				if (mark[t.node]) {
					c++;
					d += t.weight;
					node = t.node;;
					break;
				}
			}
		}
		cout << d << endl;
	}
	return 0;
}