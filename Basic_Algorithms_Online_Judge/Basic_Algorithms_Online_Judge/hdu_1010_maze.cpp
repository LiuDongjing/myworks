#include <iostream>
#include <vector>
using namespace std;
bool travel(vector<vector<char> > &maze, 
		vector<vector<bool> > &mark, 
		int t, int len, int x, int y, int dx, int dy) {
	if (x < 0 || x >= maze.size() || y < 0 || y >= maze[0].size()) {
		return false;
	}
	if (maze[x][y] == 'D') {
		if (len == t) {
			return true;
		}
		return false;
	}
	if (!mark[x][y]) return false;
	// 这个地方要剪枝，不然会TLE
	// 从当前位置到大目标位置，最少需要abs(x-dx)+abs(y-dy)步；为了凑够
	// t-len步，离开最短路径再回归最短路径的步数一定是偶数。
	int tmp = t - len - (abs(dx - x) + abs(dy - y));
	if (tmp < 0 || tmp & 1) return false;
	char c = maze[x][y];
	if (c == 'S' || c == '.') {
		mark[x][y] = false;
		len++;
		bool f = false;
		f = travel(maze, mark, t, len, x + 1, y, dx, dy)
			|| travel(maze, mark, t, len, x - 1, y, dx, dy)
			|| travel(maze, mark, t, len, x, y + 1, dx, dy)
			|| travel(maze, mark, t, len, x, y - 1, dx, dy);
		mark[x][y] = true;
		len--;
		return f;
	}
	return false;
}
int main() {
#ifdef _DEBUG
	freopen("hdu_1010_maze.txt", "r", stdin);
#endif
	int n, m, t;
	while (0 < scanf("%d%d%d", &n, &m, &t)) {
		if (n == 0) break;
		vector<vector<char> > maze(n, vector<char>(m));
		vector<vector<bool> > mark(n, vector<bool>(m, true));
		char *tmp = new char[m + 1];
		int si, sj, di, dj;
		for (int i = 0; i < n; i++) {
			scanf("%s", tmp);
			for (int j = 0; j < m; j++) {
				maze[i][j] = tmp[j];
				if (tmp[j] == 'S') {
					si = i;
					sj = j;
				}
				if (tmp[j] == 'D') {
					di = i;
					dj = j;
				}
			}
		}
		delete tmp;
		if (travel(maze, mark, t, 0, si, sj, di, dj)) {
			printf("YES\n");
		}
		else {
			printf("NO\n");
		}
	}
	return 0;
}