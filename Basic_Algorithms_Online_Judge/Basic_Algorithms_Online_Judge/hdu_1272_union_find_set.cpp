#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
void reset(vector<int> & set) {
	for (int i = 0; i < set.size(); i++) {
		set[i] = -1;
	}
}
int find(vector<int> & set, int v) {
	if (set[v] < 0) return set[v];
	if (set[v] == v) {
		return v;
	}
	int k = find(set, set[v]);
	set[v] = k;
	return k;
}
int main() {
#ifdef _DEBUG
	freopen("hdu_union_find_set.txt", "r", stdin);
#endif
	int a, b;
	vector<int> set(100001);
	while (scanf("%d%d", &a, &b) > 0) {
		if (a < 0) break;
		reset(set);
		int mx = a;
		bool f = true;
		while (a > 0) {
			mx = max(mx, max(a, b));
			if (f) {//保证无环
				int x = find(set, a);
				int y = find(set, b);
				if (x >= 0 && y >= 0) {
					if (x == y) {
						f = false;
					}
					else {
						set[y] = x;
					}
				}
				else if (x >= 0 && y < 0) {
					set[b] = x;
				}
				else if (x < 0 && y >= 0) {
					set[a] = y;
				}
				else {
					set[a] = a;
					set[b] = a;
				}
			}
			scanf("%d%d", &a, &b);
		}
		if (f) {
			// 保证所有点都连通
			int p = find(set, mx);
			for (int i = 1; i <= mx; i++) {
				int t = find(set, i);
				if (t >= 0 && t != p) {
					f = false;
					break;
				}
			}
		}
		if (f) {
			printf("Yes\n");
		}
		else {
			printf("No\n");
		}
	}
	return 0;
}