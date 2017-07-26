#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>
using namespace std;
//��index��[start, end)��Χ�����ݽ��л��֣��������ڻ��ֵ����ֵ�
//index.
int partition(vector<int> &data, int start, int end) {
	int index = start + rand() % (end - start);
	int val = data[index];
	swap(data[index], data[end - 1]);
	int i = start, j = end - 2;
	while (i < j) {
		for (; i < end-1 && data[i] <= val; i++);
		for (; j >= 0 && data[j] > val; j--);
		if (i < j) swap(data[i++], data[j--]);
	}
	swap(data[i], data[end - 1]);
	return i;
}
void quick_sort(vector<int> &data, int start, int end) {
	if (start >= end) return;
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