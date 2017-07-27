#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>
using namespace std;
//对index在[start, end)范围的数据进行划分，返回用于划分的数字的
//index.
int partition(vector<int> &data, int start, int end) {
	int index = start + rand() % (end - start);
	int val = data[index];
	swap(data[index], data[end-1]);
	int low_bnd = start;
	for (int i = start; i < end-1; i++) {
		if (data[i] <= val) {
			if (low_bnd != i) swap(data[low_bnd], data[i]);
			low_bnd++;
		}
	}
	swap(data[low_bnd], data[end - 1]);
	return low_bnd;
}
void quick_sort(vector<int> &data, int start, int end) {
	if (start >= end-1) return;
	int split = partition(data, start, end);
	if (split - 1 > start)
		quick_sort(data, start, split);
	if (split + 1 < end)
		quick_sort(data, split + 1, end);
}
int main() {
	freopen("hdu_1040_quick_sort.txt", "r", stdin);
	srand(time(0));
	int cases;
	cin >> cases;
	for (; cases > 0; cases--) {
		int n;
		cin >> n;
		vector<int> data(n);
		for (int i = 0; i < n; i++)
			cin >> data[i];
		quick_sort(data, 0, n);
		cout << data[0];
		for (int i = 1; i < data.size(); i++)
			cout << ' ' << data[i];
		cout << endl;
	}
	return 0;
}