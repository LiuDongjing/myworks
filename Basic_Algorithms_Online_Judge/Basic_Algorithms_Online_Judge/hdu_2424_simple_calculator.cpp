#include <iostream>
#include <string>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;
string add(const string &a, const string &b) {
	string ra = a, rb = b;
	string res;
	reverse(ra.begin(), ra.end());
	reverse(rb.begin(), rb.end());
	int c = 0;
	for (int i = 0; i < max(ra.size(), rb.size()); i++) {
		int x = 0, y = 0;
		if (i < ra.size()) {
			x = ra[i] - '0';
		}
		if (i < rb.size()) {
			y = rb[i] - '0';
		}
		res.push_back(('0' + (x + y + c) % 10));
		c = (x + y + c) / 10;
	}
	if (c > 0) {
		res.push_back('0' + c);
	}
	reverse(res.begin(), res.end());
	return res;
}
string mul(const string &a, const string &b) {
	int s1 = a.size(), s2 = b.size();
	string res(s1+s2, '0');
	string ra = a, rb = b;
	reverse(ra.begin(), ra.end());
	reverse(rb.begin(), rb.end());
	for (int i = 0; i < s1; i++) {
		int c = 0;
		for (int j = 0; j < s2; j++) {
			int z = j + i;
			int r = (ra[i] - '0')*(rb[j] - '0')+(res[z]-'0') + c;
			res[z] = '0'+(r % 10);
			c = r / 10;
		}
		if (c > 0) {
			//最多进位两次
			int z = s2 + i;
			int r = (res[z] - '0') + c;
			res[z] = '0' + (r % 10);
			c = r / 10;
			if (c > 0) {
				z++;
				res[z] += c;
			}
		}
	}
	if (res.back() == '0') {
		res.erase(s1+s2-1);
	}
	reverse(res.begin(), res.end());
	return res;
}
bool eval_exp(vector<string> &exp, string &val) {
	if (exp.size() % 2 == 0) {
		return false;
	}
	val = "";
	stack<string> op_stk, num_stk;
	for (int i = 0; i < exp.size(); i++) {
		string &t = exp[i];
		if (i % 2 == 0) {
			if (t[0] < '0' || t[0] > '9') {
				return false;
			}
			if (op_stk.empty() || op_stk.top()[0] == '+') {
				num_stk.push(t);
			}
			else {
				if (num_stk.empty()) {
					return false;
				}
				string v = num_stk.top();
				num_stk.pop();
				op_stk.pop();
				num_stk.push(mul(v, t));
			}
		}
		else {
			if (t[0] != '+' && t[0] != '*') {
				return false;
			}
			op_stk.push(t);
		}
	}
	val = "0";
	while (!num_stk.empty()) {
		string &t = num_stk.top();
		val = add(val, t);
		num_stk.pop();
	}
	return true;
}
int main() {
#ifdef _DEBUG
//	freopen("hdu_2424_simple_calculator.txt", "r", stdin);
#endif
	int n;
	int cases = 0;
	while (0 < scanf("%d", &n)) {
		vector<string> exp;
		cases++;
		for (int i = 0; i < n; i++) {
			string t;
			cin >> t;
			exp.push_back(t);
		}
		string val;
		if (eval_exp(exp, val)) {
			printf("Case %d: %s\n", cases, val.c_str());
		}
		else {
			printf("Case %d: Invalid Expression!\n", cases);
		}
	}
	return 0;
}