from utils import Utils

code = '''
function g() {
    print(2);
}

g();

'''

utils = Utils()
result = utils.run_expression(code)
print(result)
