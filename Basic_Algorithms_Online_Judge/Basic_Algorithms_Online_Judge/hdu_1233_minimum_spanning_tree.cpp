#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class Edge {
public:
	Edge() {
		u = 0;
		v = 0;
		w = 0;
	}
	Edge(int uu, int vv, int ww) {
		u = uu;
		v = vv;
		w = ww;
	}
	int u;
	int v;
	int w;
};
bool cmp(Edge &a, Edge &b) {
	return a.w < b.w;
}
int find(vector<int> &ufs, int id) {
	if (id == ufs[id]) {
		return id;
	}
	int x =  find(ufs, ufs[id]);
	ufs[id] = x;
	return x;
}
int merge(vector<int> &ufs, int x, int y) {
	ufs[x] = y;
	return y;
}
int main() {
#ifdef _DEBUG
	freopen("hdu_1233_minimum_spanning_tree.txt", "r", stdin);
#endif
	int n;
	while (scanf("%d", &n) > 0) {
		if (n <= 0) break;
		int t = n*(n - 1) / 2;
		vector<Edge> edges(t);
		for (int i = 0; i < t; i++) {
			int a, b, c;
			scanf("%d%d%d", &a, &b, &c);
			edges[i].u = a;
			edges[i].v = b;
			edges[i].w = c;
		}
		vector<int> ufs(n + 1);
		for (int i = 0; i < ufs.size(); i++) {
			ufs[i] = i;
		}
		sort(edges.begin(), edges.end(), cmp);
		int cost = 0;
		int count = 0;
		for (int i = 0; i < edges.size(); i++) {
			auto &e = edges[i];
			int x = find(ufs, e.u), y = find(ufs, e.v);
			if (x != y) {
				cost += e.w;
				count++;
				merge(ufs, x, y);
			}
			if (count >= n - 1) {
				break;
			}
		}
		printf("%d\n", cost);
	}
	return 0;
}