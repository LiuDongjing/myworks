#include <iostream>
#include <vector>
using namespace std;
int main() {
#ifdef _DEBUG
	freopen("spoj_binary_search.txt", "r", stdin);
#endif
	int n, q;
	scanf("%d%d", &n, &q);
	vector<int> data(n);
	for (int i = 0; i < n; i++)
		scanf("%d", &data[i]);
	for (int i = 0; i < q; i++) {
		int e;
		int index = -1;
		int low = 0, high = n;
		scanf("%d", &e);
		while (low < high) {
			int m = (low + high) / 2;
			if (data[m] < e) {
				low = m + 1;
			}
			else if (data[m] > e) {
				high = m;
			}
			else {
				high = m;
				index = m;
			}
		}
		printf("%d\n", index);
	}
	return 0;
}