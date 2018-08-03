## 钱包使用

打开钱包

```
open wallet neo-privnet.sample.wallet
```

创建自己的钱包

```
create wallet workshop-example
```



转账

```
send neo {address} 10000 # 发送neo
send gas {address} 10000 # 发送gas
```



## 合约测试+部署

###编译和测试

打开合约事件日志`config sc-events on`

合约编译命令格式

 `build path/to/file.py test {input_params} {return_type} {needs_storage} {needs_dynamic_invoke} param1 param2 etc..`

- `{input_params}` 

  输入参数类型(参数类型表的值之一)

  ​

- `{return_type}` 

  返回值类型(参数类型表的值之一)

  ​

- `{needs_storage}` 

  True/False: 合约是否需要用到存储

  ​

- `{needs_dynamic_invoke}` 

  合约是否需要用到动态调用（绝大多数情况下是False)

  is also a boolean, indicating whether or not the SC will be calling another contract whose address it will not know until runtime. This will most always be `False`

  动态调用可以允许调用直到runtime之前都没有发布的合约。

  ​

- `params1 params2 etc...` 

  传入合约的参数

#### 参数类型表

| 参数类型             | 参数类型表示值 |
| ---------------- | ------- |
| Signature        | 00      |
| Boolean          | 01      |
| Integer          | 02      |
| Hash160          | 03      |
| Hash256          | 04      |
| ByteArray        | 05      |
| PublicKey        | 06      |
| String           | 07      |
| Array            | 10      |
| InteropInterface | f0      |
| void             | ff      |



### 部署和调用

部署.avm格式合约:

`import contract path/to/sample2.avm {input_params} {return_type} {needs_storage} {needs_dynamic_invoke}`

注意无需传入参数

输入合约的一些信息

输入密码以确认部署

部署完成后的合约存储于区块链上，无法改变

**调用**

调用合约时需要知道这个合约的hash，通过

`contract search {contract_info}`可以查找合约。此外contract_hash也可以在合约完成发布时的日志里找到。

通过hash调用合约：

`testinvoke {contract_hash} {input_parameters}`



### 例子

可从这里下载[]。放入`./neo-local/smart-contracts/`文件夹内

- **Print and Notify**

```python
def Main():
    # Print translates to a `Log` call, and is best used with simple strings for
    # development info. To print variables such as lists and objects, use `Notify`.
    print("log via print (1)"07)
    Log("normal log (2)")
    Notify("notify (3)")

    # Sending multiple arguments as notify payload:
    msg = ["a", 1, 2, b"3"]
    Notify(msg)
```

`print()`是Python内置的打印函数，`Log()`和`Notify()`同样是打印输出，不同的是`Notify()`可以打印`object`对象，上面我们用`Notify()`打印了一个数组。

- **Calculator**

```python
def Main(operation, a, b):

    if operation == 'add':
        return a + b

    elif operation == 'sub':
        return a - b

    elif operation == 'mul':
        return a * b

    elif operation == 'div':
        return a / b

    else:
        return -1
```

070202 02

- **Storage**

  note: NEO智能合约的存储是通过键-值存储。

```python
from boa.interop.Neo.Storage import Get,Put,Delete,GetContext

def Main(operation, addr, value):


    if not is_valid_addr(addr):
        return False

    context = GetContext()

    if operation == 'add':
        balance = Get(context, addr)
        new_balance = balance + value
        Put(context, addr, new_balance)
        return new_balance

    elif operation == 'remove':
        balance = Get(context, addr)
        Put(context, addr, balance - value)
        return balance - value

    elif operation == 'balance':
        return Get(context, addr)

    return False

def is_valid_addr(addr):

    if len(addr) == 20:
        return True
    return False
```

`Get(context, key)`是通过上下文使用指定key获取值，`Put(context, key, value)`是通过上下文用指定key将value给存储或更新，`Delete(context, key)`是通过上下文用删除指定key存储的值。



输入参数为 字符串 字节数组 整数。输出参数为 整数

注意当处理地址时，可以输入地址的字符串(string)形式或字节数组(bytearray)形式



- **Domain域名服务**

  此智能合约通过使用区块链的存储系统，给钱包地址提供域名服务。每个注册的域名对应一个地址。

  合约有以下功能：

  - 域名注册
  - 域名查询
  - 删除一个域名
  - 转让域名的所有权

  ```python

  from boa.interop.Neo.Runtime import Log, Notify
  from boa.interop.Neo.Storage import Get, Put, GetContext
  from boa.interop.Neo.Runtime import GetTrigger,CheckWitness
  from boa.builtins import concat


  def Main(operation, args):
      nargs = len(args)
      if nargs == 0:
          print("No domain name supplied")
          return 0

      if operation == 'query':
          domain_name = args[0]
          return QueryDomain(domain_name)

      elif operation == 'delete':
          domain_name = args[0]
          return DeleteDomain(domain_name)

      elif operation == 'register':
          if nargs < 2:
              print("required arguments: [domain_name] [owner]")
              return 0
          domain_name = args[0]
          owner = args[1]
          return RegisterDomain(domain_name, owner)

      elif operation == 'transfer':
          if nargs < 2:
              print("required arguments: [domain_name] [to_address]")
              return 0
          domain_name = args[0]
          to_address = args[1]
          return TransferDomain(domain_name, to_address)


  def QueryDomain(domain_name):
      msg = concat("QueryDomain: ", domain_name)
      Notify(msg)

      context = GetContext()
      owner = Get(context, domain_name)
      if not owner:
          Notify("Domain is not yet registered")
          return False

      Notify(owner)
      return owner


  def RegisterDomain(domain_name, owner):
      msg = concat("RegisterDomain: ", domain_name)
      Notify(msg)

      if not CheckWitness(owner):
          Notify("Owner argument is not the same as the sender")
          return False

      context = GetContext()
      exists = Get(context, domain_name)
      if exists:
          Notify("Domain is already registered")
          return False

      Put(context, domain_name, owner)
      return True


  def TransferDomain(domain_name, to_address):
      msg = concat("TransferDomain: ", domain_name)
      Notify(msg)

      context = GetContext()
      owner = Get(context, domain_name)
      if not owner:
          Notify("Domain is not yet registered")
          return False

      if not CheckWitness(owner):
          Notify("Sender is not the owner, cannot transfer")
          return False

      if not len(to_address) != 34:
          Notify("Invalid new owner address. Must be exactly 34 characters")
          return False

      Put(context, domain_name, to_address)
      return True


  def DeleteDomain(domain_name):
      msg = concat("DeleteDomain: ", domain_name)
      Notify(msg)

      context = GetContext()
      owner = Get(context, domain_name)
      if not owner:
          Notify("Domain is not yet registered")
          return False

      if not CheckWitness(owner):
          Notify("Sender is not the owner, cannot transfer")
          return False

      Delete(context, domain_name)
      return True

  ```




  - 在`Main(operation, args)`函数中，通过不同的`operation`来调用不同的函数进行操作，并进行参数校验。
  - `QueryDomain(domain_name)`：进行域名查询操作，通过`domain_name`查询所对应的地址，若对应地址存在，则返回查询到的地址，否则返回`False`。
  - `RegisterDomain(domain_name, owner)`：注册域名，我们应该只能自己当前钱包的地址进行注册等操作，所以使用`CheckWitness(owner)`进行核验，核验地址是否为当前钱包所有，然后判断域名是否已经被注册。
  - `TransferDomain(domain_name, to_address)`：域名转让，将域名`domain_name`转让到新地址`to_address`上。首先校验被转让的域名是否已经注册存在，不存在的域名是无法转让的、然后检验新地址是否为当前钱包所有，不是自己的域名是无法转让的、最后检验新地址长度是否合法。
  - `DeleteDomain(domain_name)`：删除域名，首先校验域名是否存在，然后校验域名是否为当前钱包所有，否则不能删除。

编译：注意输入参数为字符串和数组，输出参数为字节数组

  ```
build smart-contracts/5-domain.py 0710 05 True False
  ```

部署

```
import contract smart-contracts/5-domain.avm 0710 05 True False
```

调用

```
testinvoke {contract_hash} register ['domain.com', 'ATZE8izvnGGuxLYRZUDPwFr6yqyaBavVWV']
```

因为合约返回的地址为字节数组，所以需要用一个线上工具来转换：https://peterlinx.github.io/DataTransformationTools/





