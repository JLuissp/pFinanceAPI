import json
import re
import string

def extract_dict(s) -> list:
    """Extract all valid dicts from a string.
    
    Args:
        s (str): A string possibly containing dicts.
    
    Returns:
        A list containing all valid dicts.
    
    """
    results = []
    s_ = ' '.join(s.split('-,')).strip()
    exp = re.compile(r'(\{.*?\})')
    for i in exp.findall(s_):
        try:
            results.append(json.loads(i))        
        except json.JSONDecodeError:
            pass    
    return results



string = '''
{"date": "null", "concept":"uno", "pay_method":0, "transaction_type":0, "amount":-1}-,{"date": "null", "concept":"dos", "pay_method":0, "transaction_type":0, "amount":-2}-
'''


json_file = extract_dict(string)
for js in json_file:
    print(type(js))
