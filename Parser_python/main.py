from utils import Utils

code = '''
a = 1;

while (a < 10) {
    print(a);
    a = a + 1;
}
'''

utils_ = Utils()
result = utils_.run_expression(code)
print(result)
