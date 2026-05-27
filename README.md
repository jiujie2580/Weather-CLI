# Weather CLI

一个简单的命令行天气查询工具，使用 OpenWeather 获取城市当前天气。

## 准备工作

1. 注册并获取 OpenWeather API key。
2. 在终端里设置环境变量：

```powershell
$env:OPENWEATHER_API_KEY = "你的_API_KEY"
```

## 直接运行

```powershell
python weather.py London
python weather.py Beijing --timeout 5
```

也可以只在本次运行时传入 key：

```powershell
python weather.py London --api-key 你的_API_KEY
```

## 安装成本地命令

```powershell
python -m pip install -e .
weather-cli London
```

## 运行测试

```powershell
python -m unittest discover tests
```

## 已改进内容

- 不再把 API key 写死在代码里。
- 不再依赖额外安装的 `requests` 包。
- 网络失败、超时、接口返回错误时会显示清楚的错误信息。
- 增加了基础测试，方便后续修改时确认功能没有坏。
- 增加了项目配置，可以安装成本地命令行工具。