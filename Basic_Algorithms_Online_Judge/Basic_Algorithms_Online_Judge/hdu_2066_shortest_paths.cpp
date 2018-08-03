#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
vector<vector<int>> mat(1001, vector<int>(1001));
int n = 1000;
void reset() {
	for (int i = 0; i <= n; i++)
		for (int j = 0; j <= n; j++)
			if (i == j) mat[i][j] = 0;
			else mat[i][j] = -1;
}
int dijkstra(vector<int> &src, vector<int>&des) {
	vector<int> dis(n + 1, -1);
	dis[0] = 0;
	for (int i = 0; i < src.size(); i++)
		dis[src[i]] = 0;
	vector<int> left;
	for (int i = 1; i <= n; i++) left.push_back(i);
	while (left.size()) {
		int min_ind = -1;
		for (int i = 0; i < left.size(); i++) {
			if (dis[left[i]] >= 0 && (min_ind < 0 || dis[left[i]] < dis[left[min_ind]])) {
				min_ind = i;
			}
		}
		if (min_ind < 0) break;
		int k = left[min_ind];
		swap(left[min_ind], left[left.size() - 1]);
		left.pop_back();
		for (int i = 0; i < left.size(); i++) {
			int l = left[i];
			if (mat[k][l] >= 0) {
				if (dis[l] < 0 || dis[l] > dis[k] + mat[k][l]) {
					dis[l] = dis[k] + mat[k][l];
				}
			}
		}
	}
	int min_dis = -1;
	for (int i = 0; i < des.size(); i++) {
		if (dis[des[i]] >= 0) {
			if (min_dis < 0 || dis[des[i]] < min_dis) {
				min_dis = dis[des[i]];
			}
		}
	}
	return min_dis;
}
int floyd(vector<int>&src, vector<int> &des) {
	vector < vector<int> > d1 = mat, d2 = mat;
	vector<vector<int>> *prev = &d1, *curr = &d2;
	for (int k = 1; k <= n; k++) {
		for (int i = 1; i <= n; i++) {
			for (int j = i + 1; j <= n; j++) {
				int t = -1;
				if ((*prev)[i][k] >= 0 && (*curr)[k][j] >= 0) {
					t = (*prev)[i][k] + (*curr)[k][j];
				}
				if (t >= 0 && ((*prev)[i][j] < 0 || (*prev)[i][j] > t)) {
					(*curr)[i][j] = t;
					(*curr)[j][i] = t;
				}
				else {
					(*curr)[i][j] = (*curr)[j][i] = (*prev)[i][j];
				}
			}
		}
		swap(curr, prev);
	}
	int min_dis = -1;
	for (int i = 0; i < src.size(); i++) {
		for (int j = 0; j < des.size(); j++) {
			int t = (*prev)[src[i]][des[j]];
			if (t >= 0 && (min_dis < 0 || min_dis > t)) min_dis = t;
		}
	}
	return min_dis;
}
int main() {
	int t, s, d;
	while (0 < scanf("%d%d%d", &t, &s, &d)) {
		reset();
		n = 0;
		for (int i = 0; i < t; i++) {
			int a, b, tm;
			scanf("%d%d%d", &a, &b, &tm);
			n = max(n, max(a, b));
			if (mat[a][b] < 0 || tm < mat[a][b]) {
				mat[a][b] = mat[b][a] = tm;
			}
		}
		vector<int> src(s), des(d);
		for (int i = 0; i < s; i++) scanf("%d", &src[i]);
		for (int i = 0; i < d; i++) scanf("%d", &des[i]);
		printf("%d\n", floyd(src, des));
	}
	return 0;
}
