#include <iostream>
#include <vector>
#include <string>
#include <stack>
#include <cmath>

using namespace std;
bool next_num(const string &str, bool &is_int, int &s, float &num) {
	num = 0;
	is_int = true;
	if (str[s] == '.' &&
		(s + 1 >= str.size() ||
		str[s + 1] < '0' || str[s + 1] > '9')) {
		//对应着'.'开头的非法格式
		return false;
	}
	for (;
		s < str.size() && '0' <= str[s] && str[s] <= '9';
		s++) {
		num = num * 10 + (str[s] - '0');
	}
	if (str[s] == '.') {
		s++;
		is_int = false;
		float w = 10;
		for (; s < str.size() && '0' <= str[s] && str[s] <= '9';
			s++, w*=10) {
			num += (str[s] - '0') / w;
		}
	}
	return true;
}
class Node {
public:
	int type = 0;
	union {
		int idat;
		float fdat;
		char cdat;
	} data;
}; 
bool eval_infix(vector<Node> &infix, float &val) {
	stack<Node> num;
	for (int i = 0; i < infix.size(); i++) {
		Node &t = infix[i];
		if (t.type == 2) {
			if (num.empty()) {
				return false;
			}
			Node v1 = num.top();
			num.pop();
			if (num.empty()) {
				return false;
			}
			Node v2 = num.top();
			num.pop();
			char op = t.data.cdat;
			float y1, y2;
			if (v1.type == 0) {
				y1 = v1.data.idat;
			}
			else {
				y1 = v1.data.fdat;
			}
			if (v2.type == 0) {
				y2 = v2.data.idat;
			}
			else {
				y2 = v2.data.fdat;
			}
			float v;
			if (op == '+') {
				v = y1 + y2;
			}
			else if(op == '-') {
				v = y2 - y1;
			}
			else if (op == '*') {
				v = y1 * y2;
			}
			else if (op == '/') {
				if (abs(y1) < 10e-9) {
					//不能除0
					return false;
				}
				v = y2 / y1;
			}
			else if (op == '%') {
				if (v1.type != 0 || v2.type != 0
					|| abs(y1) < 10e-9) {
					//都是整数且不能模0
					return false;
				}
				v = int(y2) % int(y1);
			}
			else {
				return false;
			}
			Node x;
			if (v1.type == 0 && v2.type == 0) {
				if (op != '/') {
					x.type = 0;
					x.data.idat = v;
				}
				else {
					x.type = 1;
					x.data.fdat = v;
				}
			}
			else {
				x.type = 1;
				x.data.fdat = v;
			}
			num.push(x);
		}
		else {
			num.push(t);
		}
	}
	if (num.empty()) {
		return false;
	}
	Node v = num.top();
	num.pop();
	if (!num.empty()) return false;
	if (v.type == 0) {
		val = v.data.idat;
	}
	else {
		val = v.data.fdat;
	}
	return true;
}
bool suffix2infix(vector<Node> &infix, string &exp) {
	stack<char> stk;
	int i = 0;
	int factor = 1;
	while (i < exp.size()) {
		char c = exp[i];
		Node t;
		if (c == '.' || ('0' <= c && c <= '9')) {
			bool is_int;
			float num;
			if (next_num(exp, is_int, i, num)) {
				if (is_int) {
					t.type = 0;
					t.data.idat = int(factor*num);
				}
				else {
					t.type = 1;
					t.data.fdat = factor*num;
				}
				infix.push_back(t);
				factor = 1;
			}
			else {
				return false;
			}
			continue;
		}
		else if (c == '(') {
			stk.push(c);
		}
		else if (c == ')') {
			if (i - 1 >= 0 && exp[i - 1] == '(') {
				return false;//配对的空括号
			}
			bool match = false;
			while (!stk.empty()) {
				char x = stk.top();
				stk.pop();
				if (x == '(') {
					match = true;
					break;
				}
				t.type = 2;
				t.data.cdat = x;
				infix.push_back(t);
			}
			if (!match) {
				return false;
			}
		}
		else if (c == '+' || c == '-') {
			if ((i == 0 || exp[i - 1] == '(')) {
				if (i + 1 >= exp.size()) {
					return false;
				}
				char x = exp[i + 1];
				if (x == '.' || '0' <= x && x <= '9') {
					//+和-表示数字的符号
					if (c == '-') {
						factor = -1;
					}
					i++;
					continue;
				}
			}
			while (!stk.empty()) {
				char &x = stk.top();
				if (x == '(') {
					break;
				}
				t.type = 2;
				t.data.cdat = x;
				infix.push_back(t);
				stk.pop();
			}
			stk.push(c);
		}
		else if (c == '*' || c == '/' || c == '%') {
			while (!stk.empty()) {
				char &x = stk.top();
				if (x == '(' || x == '+' || x == '-') {
					break;
				}
				t.type = 2;
				t.data.cdat = x;
				infix.push_back(t);
				stk.pop();
			}
			stk.push(c);
		}
		else {
			return false;
		}
		i++;
	}
	while (!stk.empty()) {
		char c = stk.top();
		stk.pop();
		Node t;
		t.type = 2;
		t.data.idat = c;
		infix.push_back(t);
	}
	return true;
}
int main() {
#ifdef _DEBUG
	freopen("hdu_2556_simple_desk_calculator.txt", "r", stdin);
#endif
	string exp;
	while (cin >> exp) {
		vector<Node> infix;
		float val;
		if (!suffix2infix(infix, exp) || !eval_infix(infix, val)) {
			printf("ERROR IN INFIX NOTATION\n");
		}
		else {
			printf("%.2f\n", val);
		}
	}
	return 0;
}