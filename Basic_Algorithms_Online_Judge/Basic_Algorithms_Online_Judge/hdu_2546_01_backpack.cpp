#include <iostream>
#include <vector>
using namespace std;
int main() {
#ifdef _DEBUG
	freopen("hdu_2546_01_backpack.txt", "r", stdin);
#endif
	int n;
	while (scanf("%d", &n) > 1) {
		if (n <= 0) break;
		vector<int> price(n-1);
		int max_val = 0;
		for (int i = 0; i < n; i++) {
			scanf("%d", &price[i]);
		}
		int m;
		scanf("%d", &m);

	}
	return 0;
}