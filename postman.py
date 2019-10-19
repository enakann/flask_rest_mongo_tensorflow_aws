import requests
import sys

def req(method='post',data=None,endpoint='add'):
    headers={'Content-Type':'application/json'}
    url='http://0.0.0.0:5000/'
    url=url+'{}'.format(endpoint)
    if method == 'post':
        r=requests.post(url=url,data=data,headers=headers)
    else:
        r=requests.get(url,data=data,headers=headers)

    return r.json()





if __name__ == '__main__':

    method = sys.argv[1] if sys.argv[1] else 'post'
    data=sys.argv[2] if sys.argv[2] else '{"x": 1, "y": 2}'
    endpoint=sys.argv[3] if sys.argv[3] else 'add' 
    
    ret=req(method,data,endpoint)
    print(ret)
