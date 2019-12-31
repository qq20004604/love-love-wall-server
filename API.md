# 版本

## 已完成功能：

1. 注册
2. 发送账号激活邮件；
3. 重新发送账号激活邮件；
4. 登录；
5. 忘记密码（申请发送重置密码邮件）；
6. 验证重置密码的链接；
7. 重置密码；
8. 登出


## 接口说明

### 1、注册

说明：

```
注册接口。
当用户需要注册一个新账号的时候使用
JSON格式提交
POST
```

链接：

```
/register
```

入参：

```
{
	email: '',		//  邮箱地址，长度需要在4~60位之间
	phone: '',		// 手机号码，长度需要11位
	password: '',		// 密码，密码长度需要在8~40位之间
}
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '用户注册成功，已发送激活邮件，请访问邮箱打开激活邮件以激活账号'
   }
}
```

### 2、登录

说明：

```
登录接口。
当用户需要登录的时候使用
JSON格式提交
POST
```

链接：

```
/login
```

入参：

```
{
	email: '',		//  邮箱地址，长度需要在4~60位之间
	password: '',		// 密码，密码长度需要在8~40位之间
}
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '用户注册成功，已发送激活邮件，请访问邮箱打开激活邮件以激活账号'
   }
}
```

### 3、账号激活

说明：

```
账号激活功能
【非接口】，而是账号激活邮件里的链接
GET
```

链接：

```
/activate_account
```

入参：

```
email: '',		//  邮箱地址，长度需要在4~60位之间
vcode: '',		// 账号激活码（随机生成）
```

出参：

```
一个html文本
```

### 4、再次发送账号激活邮件

说明：

```
再次发送账号激活邮件接口
当用户没有接收到账号激活邮件时使用
JSON格式提交
POST
```

链接：

```
/send_activate_email
```

入参：

```
{
	email: ''		//  邮箱地址，长度需要在4~60位之间
}
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '已再次发送激活邮件，请访问邮箱打开激活邮件以激活账号'
   }
}
```


### 5、发送密码重置邮件

说明：

```
发送密码重置邮件接口
当用户丢失密码，或者想要更改密码时使用
JSON格式提交
POST
```

链接：

```
/reset_password/send_mail
```

入参：

```
{
	email: ''		//  邮箱地址，长度需要在4~60位之间
}
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '已发送密码重置邮件，请访问邮箱，打开邮件中的链接地址'
   }
}
```

### 6、密码重置的链接验证

说明：

```
密码重置的链接验证
【非接口】，而是重置密码邮件里的链接
GET
```

链接：

```
/reset_password/verify
```

入参：

```
email: '',		//  邮箱地址，长度需要在4~60位之间
vcode: '',		// 账号激活码（随机生成）
```

出参：

```
一个html文本
```

### 7、密码重置

说明：

```
密码重置功能
拿取密码重置链接后，输入邮箱、密码等，用于重置密码时调用（依赖前置接口5、6）
JSON格式提交
POST
```

链接：

```
/reset_password/reset
```

入参：

```
{
	email: '',		//  邮箱地址，长度需要在4~60位之间
	vcode: '',		// 账号激活码（随机生成），会写在页面里，或者从链接里获取
	password: '',		// 密码，密码长度需要在8~40位之间
	rp_password: '',		// 重复密码，需要和密码保持一致
}
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '密码重置成功'
   }
}
```

### 8、登出

说明：

```
登出功能
清除用户登录状态时使用
POST
```

链接：

```
/logout
```

入参：

```
无
```

出参：

```
{
	code: 200,	// 200表示成功，下同
	msg: 'success',		// 请求成功，但服务器处理错误，错误信息在这里。
	data: {
   		'msg': '登出成功'
   }
}
```

### 9、获取用户信息

说明：

```
获取用户信息
GET
```

链接：

```
/userinfo/get
```

入参：

```
无
```

出参：

```
{
    "code": 200,
    "msg": "success",
    "data": {
        "nickname": "nickname",
        "avatar": "avatar",
        "qq": "20004604",
        "wechat": "wechat",
        "other": "other",
        "gender": "male",
        "target_gender": "tgen",
        "age": 30,
        "target_age": "20-25",
        "tag": "tag",
        "ideal": "ideal",
        "company": "company",
        "city": "city",
        "income": "income",
        "target_income": "target_income",
        "college": "college",
        "profession": "profession",
        "summary": null,
        "is_hidden": 0,
        "hidden_columns": ['qq', 'avatar']  // 注意，nickname 不能被隐藏
    }
}
```


### 10、修改用户信息

说明：

```
修改用户信息
所有字段非必填，不填或者值为null则不会修改，但空字符串会修改该属性值
POST
```

链接：

```
/userinfo/update
```

入参：

```
{
    nickname: 'avatar',
    avatar: 'avatar',
    qq: '20004604',
    wechat: 'wechat',
    other: 'other',
    gender: 'male',
    target_gender: 'tgen',
    age: 30,
    target_age: '20-25',
    tag: 'tag',
    ideal: 'ideal',
    company: 'company',
    city: 'city',
    income: 'income',
    target_income: 'target_income',
    college: 'college',
    profession: 'profession',
    summary: 'summary',
    is_hidden: 0,
    hidden_columns: ['qq', 'avatar']
}
```

出参：

```
{
    "code": 200,
    "msg": "修改成功",
    "data": {}
}
```