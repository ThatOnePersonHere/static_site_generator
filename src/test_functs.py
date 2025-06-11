import unittest

from textnode import TextNode, TextType
from main import *

#Set to True if you want it to print all output
Debug_Print = False

def console_print_line(text):
    if Debug_Print == True:
        print(text)

class UnitTests(unittest.TestCase):
        
    def eq_test(self,test,expected_answer):
        self.assertEqual(str(test),expected_answer)

    def not_eq_test(self,test,expected_answer):
        self.assertNotEqual(test,expected_answer)

    def assert_test(self,test_item, funct):
        with self.assertRaises(ValueError):
            funct(test_item)


test_types = UnitTests()

def generate_node(node_type,parameters):
    return eval(node_type)(*parameters)

def run_test(selected_test, int_func, int_param, ext_func, node_type, input, expected_output):
    console_print_line("---------------------------------")
    console_print_line(f"Input: {input}")
    console_print_line("")
    generated_node = generate_node(node_type, input)
    try:
        if ext_func == False:
            if int_func != False:
                if int_param != False:
                    test_obj = getattr(generated_node, int_func)(generated_node)
                else:
                    test_obj = getattr(generated_node, int_func)()
            else:
                test_obj = generated_node
            results = getattr(test_types, selected_test)(test_obj,expected_output)
        elif selected_test == 'assert_test':
            results = getattr(test_types, selected_test)(generated_node,eval(ext_func))
        else:
            results = getattr(test_types, selected_test)(eval(ext_func)(generated_node),expected_output)
        console_print_line(f"Expecting: {expected_output}")
        console_print_line(f"Actual:    {results}")
        return True
    except Exception as e:
        print(e)
        print(f"Expecting: {expected_output}")
        return False


def main(Test_Cases):
    print("--======== Running Tests ========--")
    passed = 0
    failed = 0
    for test_group in Test_Cases:
        for test_case in test_group:
            correct = run_test(*test_case)
            if correct:
                console_print_line("Pass")
                passed += 1
            else:
                print("--Fail--")
                failed += 1
    print("============= RESULTS ==============")
    print(f"{passed} passed, {failed} failed")

if __name__ == "__main__":
    unittest.main()