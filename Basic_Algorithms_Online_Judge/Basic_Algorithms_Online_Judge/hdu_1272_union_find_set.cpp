#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int union_set_find(vector<int> &set, int v) {
	return set[v] == v ? v : set[v] = union_set_find(set, set[v]);
}
int main() {
#ifdef _DEBUG
	freopen("hdu_union_find_set.txt", "r", stdin);
#endif
	int a, b;
	while (scanf("%d%d", &a, &b) > 0) {
		if (a < 0) break;
		if (a == 0) {
			//printf("NO\n");
			continue;
		}
		int max_val = 0;
		vector<int> tmp;
		while (a > 0) {
			if (a > max_val) max_val = a;
			if (b > max_val) max_val = b;
			tmp.push_back(a);
			tmp.push_back(b);
			scanf("%d%d", &a, &b);
		}
		vector<int> set(max_val + 1);
		for (int i = 1; i <= max_val; i++) {
			set[i] = i;
		}
		bool yes = true;
		//保证无环
		for (int i = 0; i+1 < tmp.size(); i+=2) {
			int p1 = union_set_find(set, tmp[i]);
			int p2 = union_set_find(set, tmp[i + 1]);
			if (p1 == p2) {
				yes = false;
				break;
			}
			else {
				set[p2] = p1;
			}
		}
		//保证只有一个连通集
		for (int i = 1; i< set.size(); i++) {
			union_set_find(set, i);
		}
		sort(set.begin(), set.end());
		int c = 0;
		for (int i = 0; i < set.size();) {
			int j = i + 1;
			for (; j < set.size() && set[j] == set[i]; j++);
			if (j - i > 1) c++;
			i = j;
		}
		if (c > 1) yes = false;
		if (yes) {
			printf("YES\n");
		}
		else {
			printf("NO\n");
		}
	}
	return 0;
}