
### 版本

* **alpha-4 2023-01**: 当前版本
```
    * 基于无复权单位净值计算区间收益率 => 基于日增长率计算区间收益率
```

* **alpha-3 2023-01**
```
    * 加入了比较基准
```

* **alpha-2 2023-01**
```
    * 修正了因交易日不对导致的结果差异
```

* **alpha-1 2022-12**
```
    * 数据源从WindPy改为AKShare
    * 实现GitHub+Streamlit部署
```

### 开发流程

* **算法设计**: 本地Jupyter调试
* **本地开发**: 算法与Streamlit交互结合
* **远程部署**: Push到GitHub并进行Streamlit部署