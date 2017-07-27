#include <iostream>
#include <vector>
using namespace std;
int main() {
#ifdef _DEBUG
	freopen("spoj_binary_search.txt", "r", stdin);
#endif
	int n, q;
	cin >> n >> q;
	vector<int> data(n);
	for (int i = 0; i < n; i++)
		cin >> data[i];
	for (int i = 0; i < q; i++) {
		int e;
		int index = -1;
		int low = 0, high = n;
		cin >> e;
		while (low < high) {
			int m = (low + high) / 2;
			if (data[m] < e) {
				low = m + 1;
			}
			else if (data[m] > e) {
				high = m;
			}
			else {
				if (m - 1 >= 0 && data[m - 1] == e) {
					//不是第一次出现
					high = m;
				}
				else {
					index = m;
					break;
				}
			}
		}
		cout << index << endl << endl;
	}
	return 0;
}