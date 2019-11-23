## 说明

工具类，能生成 md5 和 sha1 字符串，也可以用于比较字符串和其md5形式是否相等

## 1、使用方法：

先生成实例

```
tool = Md5Tool()
```

需要 sha1 字符串

```
s = tool.get_sha1(你的字符串)
```


需要 md5 字符串

```
s = tool.get_md5(你的字符串)
```

比较一个字符串的md5版本，和另一个md5字符串是否相等，相等则返回 True

```
isEqual = tool.is_str_md5_equal(被比较的字符串, 被比较的md5字符串）
```

比较一个字符串的 sha1 版本，和另一个 sha1 字符串是否相等，相等则返回 True

```
isEqual = tool.is_str_sha1_equal(被比较的字符串, 被比较的sha1字符串）
```