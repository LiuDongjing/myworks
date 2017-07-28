#include <iostream>
#include <vector>
using namespace std;
int main() {
#ifdef _DEBUG
	freopen("spoj_binary_search.txt", "r", stdin);
#endif
	long long n, q;
	cin >> n >> q;
	vector<long long> data(n);
	for (long long i = 0; i < n; i++)
		cin >> data[i];
	for (long long i = 0; i < q; i++) {
		long long e;
		long long index = -1;
		long long low = 0, high = n-1;
		cin >> e;
		while (low <= high) {
			long long m = (low + high) / 2;
			if (data[m] < e) {
				low = m + 1;
			}
			else if (data[m] > e) {
				high = m - 1;
			}
			else {
				high = m - 1;
				index = m;
			}
		}
		cout << index << endl;
	}
	return 0;
}