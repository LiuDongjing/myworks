#include <iostream>
#include <vector>
using namespace std;
void merge_sort(vector<int> &data, int start, int end) {
	if (start >= end - 1) return;
	int m = (start + end) / 2;
	merge_sort(data, start, m);
	merge_sort(data, m, end);
	vector<int> tmp(end - start);
	int left = start, right = m;
	for (int i = 0; i < tmp.size(); i++) {
		if (left < m && right < end) {
			if (data[left] <= data[right]) {
				tmp[i] = data[left++];
			}
			else {
				tmp[i] = data[right++];
			}
		}
		else if (left < m) {
			tmp[i] = data[left++];
		}
		else {
			tmp[i] = data[right++];
		}
	}
	for (int i = 0; i < tmp.size(); i++)
		data[start + i] = tmp[i];
}
int main() {
#ifdef _DEBUG
	freopen("hdu_1040_merge_sort.txt", "r", stdin);
#endif
	int T;
	scanf("%d", &T);
	while (T--) {
		int N;
		scanf("%d", &N);
		vector<int> data(N);
		for (int i = 0; i < N; i++)
			scanf("%d", &data[i]);
		merge_sort(data, 0, N);
		printf("%d", data[0]);
		for (int i = 1; i < N; i++) {
			printf(" %d", data[i]);
		}
		printf("\n");
	}
	return 0;
}