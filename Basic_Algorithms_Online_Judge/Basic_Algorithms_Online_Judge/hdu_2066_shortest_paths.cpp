#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

class Vertex {
public:
	int dis;
	int pre;
	int index;
	vector<int> nodes;
	vector<int> weights;
	Vertex() {
		dis = -1;
		pre = -1;
		index = -1;
	}
};
int dijkstra(vector<Vertex> &at, int n, int src, int &dt, vector<int> &dv) {
	vector<bool> mark(n + 1, true);
	mark[src] = false;
	int md = 1;
	while (md >= 0) {
		md = -1;
		int ind = -1;
		for (int i = 0; i <= n; i++) {
			if (at[i].index > 0 && mark[i] && (md < 0 || at[i].dis >= 0 && md > at[i].dis)) {
				ind = i;
				md = at[i].dis;
			}
		}
		if (ind > 0) {
			mark[ind] = false;
			for (int i = 0; i < at[ind].nodes.size(); i++) {
				int t = at[ind].dis + at[ind].weights[i];
				if (mark[at[ind].nodes[i]]&& (at[at[ind].nodes[i]].dis < 0 || at[at[ind].nodes[i]].dis > t)) {
					at[at[ind].nodes[i]].dis = t;
					at[at[ind].nodes[i]].pre = ind;
				}
			}
		}
	}
	int mt = -1;
	for (int i = 0; i < dv.size(); i++) {
		if (mt < 0 || (at[dv[i]].dis >= 0 && at[dv[i]].dis < mt)) {
			mt = at[dv[i]].dis;
			dt = dv[i];
		}
	}
	return mt;
}
void print_path(vector<Vertex> &at, int src, int des) {
	if (src == des) {
		cout << des << " ";
	}
	else {
		if (at[des].pre < 0) {
			cout << "There is no path from " << src << " to " << des;
		}
		else {
			print_path(at, src, at[des].pre);
			cout << des << " ";
		}
	}
}
int dijkstra_multi_src(vector<Vertex> &at, int n, vector<int> &sv, vector<int> &dv) {
	at[0].dis = 0;
	for (int i = 0; i < sv.size(); i++) {
		at[0].nodes.push_back(sv[i]);
		at[0].weights.push_back(0);
		at[sv[i]].dis = 0;
		at[sv[i]].pre = 0;
		at[sv[i]].nodes.push_back(0);
		at[sv[i]].weights.push_back(0);
	}
	int dt;
	int t = dijkstra(at, n, 0, dt, dv);
	//print_path(atb, st, dd);
	//cout << endl;
	return t;
}

void reset(vector<Vertex> &at, int n) {
	for (int i = 0; i <= n; i++) {
		at[i] = Vertex();
	}
}
void reset(vector<vector<int> > &mat, int sz) {
	for (int i = 1; i < sz; i++) {
		for (int j = 1; j < sz; j++) {
			if (i == j) {
				mat[i][j] = 0;
			}
			else {
				mat[i][j] = -1;
			}
		}
	}
}
void print_path(vector<vector<int> > &pai, int i, int j) {
	if (i == j) {
		cout << i << " ";
		return;
	}
	if (pai[i][j] < 0) {
		cout << "There is no path from " << i << " to " << j << endl;
	}
	else {
		print_path(pai, i, pai[i][j]);
		cout << j << " ";
	}
}
int floyd_warshall(vector<vector<int> > &mat, int n, vector<int> &sv, vector<int> &dv) {
	vector<vector<int> > *d = new vector<vector<int> >(n + 1, vector<int>(n + 1));
	vector<vector<int> > *dk = new vector<vector<int> >(n + 1, vector<int>(n + 1));
	vector<vector<int> > *p = new vector<vector<int> >(n + 1, vector<int>(n + 1));
	vector<vector<int> > *pk = new vector<vector<int> >(n + 1, vector<int>(n + 1));
	for (int i = 1; i <= n; i++) {
		for (int j = 1; j <= n; j++) {
			(*d)[i][j] = mat[i][j];
			(*dk)[i][j] = mat[i][j];
			if (mat[i][j] > 0) {
				(*p)[i][j] = i;
				(*pk)[i][j] = i;
			}
			else {
				(*p)[i][j] = -1;
				(*pk)[i][j] = -1;
			}
		}
	}
	for (int k = 1; k <= n; k++) {
		for (int i = 1; i <= n; i++) {
			for (int j = 1; j <= n; j++) {
				if (i == j) continue;
				int t = -1;
				if ((*d)[i][k] > 0 && (*d)[k][j] > 0) {
					t = (*d)[i][k] + (*d)[k][j];
				}
				(*dk)[i][j] = (*d)[i][j];
				(*pk)[i][j] = (*p)[i][j];
				if (t > 0 && ((*d)[i][j] < 0 || t < (*d)[i][j])) {
					(*dk)[i][j] = t;
					(*pk)[i][j] = k;
				}
			}
		}
		swap(d, dk);
		swap(p, pk);
	}
	int mt = -1, st, dt;
	for (int i = 0; i < sv.size(); i++) {
		for (int j = 0; j < dv.size(); j++) {
			if (mt < 0 || (*d)[sv[i]][dv[j]] > 0 && (*d)[sv[i]][dv[j]] < mt) {
				mt = (*d)[sv[i]][dv[j]];
				st = sv[i];
				dt = dv[j];
			}
		}
	}
	//print_path(*p, st, dt);
	//cout << endl;
	return mt;
}
#if 0
int main() {
#ifdef _DEBUG
	freopen("hdu_2066_shortest_paths.txt", "r", stdin);
#endif
	vector<vector<int> > mat(1001, vector<int>(1001));
	int t, s, d;
	int n = mat.size();
	while (0 < scanf("%d%d%d", &t, &s, &d)) {
		reset(mat, n);
		n = -1;
		for (int i = 0; i < t; i++) {
			int a, b, ti;
			scanf("%d%d%d", &a, &b, &ti);
			mat[a][b] = ti;
			mat[b][a] = ti;
			n = max(n, max(a, b));
		}
		vector<int> dv(d), sv(s);
		for (int i = 0; i < s; i++) {
			scanf("%d", &sv[i]);
		}
		for (int i = 0; i < d; i++) {
			scanf("%d", &dv[i]);
		}
		cout << floyd_warshall(mat, n, sv, dv) << endl;
	}
	return 0;
}
#endif
void add_edge(vector<Vertex> &at, int a, int b, int t) {
	int hit = -1;
	for (int i = 0; i < at[a].nodes.size(); i++) {
		if (at[a].nodes[i] == b) {
			hit = i;
			break;
		}
	}
	if (hit >= 0) {
		if (at[a].weights[hit] > t) {
			at[a].weights[hit] = t;
		}
	}
	else {
		at[a].nodes.push_back(b);
		at[a].weights.push_back(t);
	}
}
int main() {
#ifdef _DEBUG
	freopen("hdu_2066_shortest_paths.txt", "r", stdin);
#endif
	vector<Vertex> at(1001);
	int t, s, d;
	int n = at.size()-1;
	while (0 < scanf("%d%d%d", &t, &s, &d)) {
		reset(at, n);
		n = -1;
		for (int i = 0; i < t; i++) {
			int a, b, ti;
			scanf("%d%d%d", &a, &b, &ti);
			at[a].index = a;
			at[b].index = b;
			add_edge(at, a, b, ti);
			add_edge(at, b, a, ti);
			n = max(n, max(a, b));
		}
		vector<int> dv(d), sv(s);
		for (int i = 0; i < s; i++) {
			scanf("%d", &sv[i]);
		}
		for (int i = 0; i < d; i++) {
			scanf("%d", &dv[i]);
		}
		cout << dijkstra_multi_src(at, n, sv, dv) << endl;
	}
	return 0;
}