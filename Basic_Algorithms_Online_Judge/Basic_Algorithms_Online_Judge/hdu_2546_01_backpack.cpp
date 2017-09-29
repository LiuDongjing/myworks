#include <iostream>
#include <vector>
using namespace std;
int main() {
#ifdef _DEBUG
	freopen("hdu_2546_01_backpack.txt", "r", stdin);
#endif
	int n;
	while (scanf("%d", &n) > 0) {
		if (n <= 0) break;
		vector<int> price(n);
		int max_ind = 0;
		for (int i = 0; i < n; i++) {
			scanf("%d", &price[i]);
			if (price[i] > price[max_ind]) max_ind = i;
		}
		int m;
		scanf("%d", &m);
		if (m < 5) {
			printf("%d\n", m);
			continue;
		}
		m -= 5;
		int max_val = price[max_ind];
		swap(price[max_ind], price.back());
		price.pop_back();
		vector<int> dp(m+1, 0);
		for (int i = 0; i < n-1; i++) {
			for (int j = m; j >= price[i]; j--) {
				//必须是这种倒序，这样n和n-1才可以共用数组
				int t = dp[j - price[i]] + price[i];
				if (t > dp[j]) dp[j] = t;
			}
		}
		printf("%d\n", m - dp[m] + 5 - max_val);
	}
	return 0;
}