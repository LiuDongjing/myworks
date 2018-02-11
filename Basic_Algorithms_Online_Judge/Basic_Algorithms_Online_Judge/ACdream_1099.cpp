#include <iostream>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;
int partition(vector<int> &data, int start, int end) {
	int index = start + rand() % (end - start);//随机化，应对本来已经排好序的情况
	int val = data[index];
	swap(data[index], data[end - 1]);// 把待比较的数据放在末尾
	int low_bnd = start;//指向左边第一个小于等于val的数据
	// low_bnd左边都是比val大的数，[low_bnd, i)都是小于等于val的数，i每找到一个比val
	// 大的数，都会和low_bnd交换；这段代码保证[start, low_bnd)是大于val的数，[low_bnd, i)是
	// 小于等于val的数，i逐步增大，直到末尾。
	for (int i = start; i < end - 1; i++) {
		if (data[i] > val) {
			if (low_bnd != i) swap(data[low_bnd], data[i]);
			low_bnd++;
		}
	}
	// 最后把val放回分界线的位置
	swap(data[low_bnd], data[end - 1]);
	return low_bnd;
}
int find_k(vector<int> &data, int k) {
	//if(data.size() < k) return data[data.size() - 1];
	int i = 0, j = data.size();
	k--;// 第k大在数组中是第k-1位
	// 二分查找的思路
	while (i < j) {
		int n = partition(data, i, j);
		if (n < k) {
			i = n + 1;
		}
		else if (n > k) {
			j = n;
		}
		else {
			break;
		}
	}
	return data[k];
}
int find_kth(vector<int> &data, int k) {
	sort(data.begin(), data.end(), greater<int>());
	return data[k - 1];
}
void init(vector<int> &data) {
	for (int i = 0; i < data.size(); i++) {
		data[i] = rand() % 100000 + 1;
	}
}
void print_vec(vector<int> &data) {
	for (int i = 0; i < data.size(); i++)
		printf("%d ", data[i]);
	printf("\n");
}
void test() {
	for (int i = 0; i < 100; i++) {
		int n = rand() % 1000+1;
		vector<int> data(n);
		init(data);
		vector<int> ori = data;
		for (int j = 0; j < 5; j++) {
			int k = rand() % n + 1;
			int x = find_k(data, k);
			int y = find_kth(data, k);
			if (x != y) {
				cout << k << endl;
				print_vec(ori);
			}
		}
	}
}
int main() {
#if _DEBUG
	freopen("ACdream_1099.txt", "r", stdin);
#endif
	int n, k;
	scanf("%d%d", &n, &k);
	vector<int> data(n);
	for (int i = 0; i < n; i++) {
		scanf("%d", &data[i]);
	}
	printf("%d\n", find_k(data, k));
	return 0;
}