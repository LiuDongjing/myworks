#include <iostream>
#include <cstring>
#include <string>
#include <queue>
#include <vector>
#include <map>
#include <set>
#include <stack>
#include <cmath>
#include <cstdio>
#include <algorithm>
#include <iomanip>
#define N 40010
#define M 800010
#define LL __int64
#define inf 0x3f3f3f3f
#define lson l,mid,ans<<1
#define rson mid+1,r,ans<<1|1
#define getMid (l+r)>>1
#define movel ans<<1
#define mover ans<<1|1
using namespace std;
const LL mod = 1000000007;
const int L = 200;
string add(string a, string b) {//ֻ�������Ǹ�������� 
	string ans;
	int na[L] = { 0 }, nb[L] = { 0 };
	int la = a.size(), lb = b.size();
	for (int i = 0; i<la; i++) na[la - 1 - i] = a[i] - '0';
	for (int i = 0; i<lb; i++) nb[lb - 1 - i] = b[i] - '0';
	int lmax = la>lb ? la : lb;
	for (int i = 0; i<lmax; i++) na[i] += nb[i], na[i + 1] += na[i] / 10, na[i] %= 10;
	if (na[lmax]) lmax++;
	for (int i = lmax - 1; i >= 0; i--) ans += na[i] + '0';
	return ans;
}
string mul(string a, string b)//�߾��ȳ˷�a,b,��Ϊ�Ǹ�����  
{
	string s;
	int na[L], nb[L], nc[L], La = a.size(), Lb = b.size();//na�洢��������nb�洢������nc�洢��  
	fill(na, na + L, 0); fill(nb, nb + L, 0); fill(nc, nc + L, 0);//��na,nb,nc����Ϊ0  
	for (int i = La - 1; i >= 0; i--) na[La - i] = a[i] - '0';//���ַ�����ʾ�Ĵ�������ת��i���������ʾ�Ĵ�������  
	for (int i = Lb - 1; i >= 0; i--) nb[Lb - i] = b[i] - '0';
	for (int i = 1; i <= La; i++)
		for (int j = 1; j <= Lb; j++)
			nc[i + j - 1] += na[i] * nb[j];//a�ĵ�iλ����b�ĵ�jλΪ���ĵ�i+j-1λ���Ȳ����ǽ�λ��  
	for (int i = 1; i <= La + Lb; i++)
		nc[i + 1] += nc[i] / 10, nc[i] %= 10;//ͳһ�����λ  
	if (nc[La + Lb]) s += nc[La + Lb] + '0';//�жϵ�i+jλ�ϵ������ǲ���0  
	for (int i = La + Lb - 1; i >= 1; i--)
		s += nc[i] + '0';//����������ת���ַ���  
	return s;
}
int main() {
	cin.sync_with_stdio(false);
	string str;
	int Case = 1, n;
	string num, sum, ans;
	while (cin >> n) {
		ans = "-1";
		sum = "0", num = "0";
		if (n % 2 == 0) {
			sum = "-1";
		}
		for (int i = 0; i < n; i++) {
			cin >> str;
			if (sum == "-1") {
				continue;
			}
			if (str == "+") {
				if (i % 2 == 0) {
					sum = "-1";
					continue;
				}
				ans = "-1";
				sum = add(sum, num);
			}
			else if (str == "*") {
				if (i % 2 == 0) {
					sum = "-1";
					continue;
				}
				ans = num;
			}
			else {
				num = str;
				if (i % 2 == 1) {
					sum = "-1";
					continue;
				}
				if (ans != "-1") {
					num = mul(num, ans);
				}
			}
		}
		cout << "Case " << Case++ << ": ";
		if (sum == "-1") {
			cout << "Invalid Expression!" << endl;
		}
		else {
			cout << add(sum, num) << endl;
		}
	}
	return 0;
}