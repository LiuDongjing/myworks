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
	int i = start, j = end - 1;
	while (i < j) {
		for (; data[i] <= val; i++);
		for (; data[j] > val; j--);
		if (i < j) swap(data[i], data[j]);
	}
	return i - 1;
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
	srand(time(0));
	int cases;
	cin >> cases;
	for (; cases > 0; cases--) {
		int n;
		cin >> n;
		vector<int> data(n);
		for (int i = 0; i < n; i++)
			cin >> data[i];
		
	}

}