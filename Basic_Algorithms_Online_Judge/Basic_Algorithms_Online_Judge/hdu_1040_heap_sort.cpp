#include <iostream>
#include <vector>
using namespace std;
void heapify(vector<int> &data, int i, int size, bool ascend=true) {
	int t = i << 1;
	int min = i;
	if (t <= size && 
		(!ascend && data[t - 1] < data[min - 1] ||
		 ascend && data[t-1] > data[min-1])) {
		min = t;
	}
	t = (i << 1) + 1;
	if (t <= size && (
		!ascend && data[t - 1] < data[min - 1] ||
		 ascend && data[t-1] > data[min-1])) {
		min = t;
	}
	if (i != min) {
		swap(data[i - 1], data[min - 1]);
		heapify(data, min, size, ascend);
	}
}
void build_heap(vector<int> &data, bool ascend=true) {
	int n = data.size();
	for (int i = n / 2; i > 0; i--) {
		heapify(data, i, n, ascend);
	}
}
void heap_sort(vector<int> &data, bool ascend=true) {
	build_heap(data, ascend);
	int n = data.size();
	while(n > 1) {
		swap(data[0], data[n - 1]);
		n--;
		heapify(data, 1, n, ascend);
	}
}
int main() {
#if _DEBUG
	freopen("hdu_1040_heap_sort.txt", "r", stdin);
#endif
	int t;
	scanf("%d", &t);
	while (t--) {
		int n;
		scanf("%d", &n);
		vector<int> data(n);
		for (int i = 0; i < n; i++)
			scanf("%d", &data[i]);
		heap_sort(data, true);
		printf("%d", data[0]);
		for (int i = 1; i < n; i++)
			printf(" %d", data[i]);
		printf("\n");
	}
	return 0;
}