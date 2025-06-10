

#自定义数据集

#特别是以 Excel 格式存储的数据，你需要先将数据转换为 PyTorch 可以处理的格式，如张量（Tensor）或自定义数据集类

import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import torch.nn as nncc

# 读取 Excel 数据
df = pd.read_excel('data.xlsx')

# 提取特征和标签  使用 df 提取excel里面的单元格的值 ，直接通过列名称 查询
features=df['features'].values
labels=df['labels'].values

# 将特征和标签转换为张量 就之前excel里面转化好的张量
features_tensor = torch.tensor(features, dtype=torch.float32)  #为什么要给定.float32
labels_tensor = torch.tensor(labels, dtype=torch.int64)  # 为什么要给定.int64


# 创建自定义数据集类
class CustomDataset(Dataset):
    def __init__(self, feature,label):   #自定义方法中的参数和上面excel里面提取无关
        self.features = feature
        self.label = label

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        return self.feature[idx], self.label[idx]
    
# 实例化时，传递转化好的张量
dataset=CustomDataset(features_tensor, labels_tensor)

# 使用 DataLoader 加载数据集
DataLoader(dataset, batch_size=32, shuffle=True)

#定义小型神经网络
#torch.nn 模块中的类和函数可以用来定义神经网络层、损失函数、优化器等
model=nn.Sequential(
    nn.Linear(3,128),  # 全连接层，执行线性变换
    nn.ReLU(),  #使用ReLU激活函数 为网络引入非线性
    nn.Linear(128,1),   #将128 映射为1维
    nn.Softmax(dim=1)
)

#定义损失函数和优化器

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

#训练模型
for epoch in range(5):
    #遍历加载数据集DataLoader
    for features, labels in DataLoader(dataset, batch_size=32, shuffle=True):
        optimizer.zero_grad() # 梯度清零
        outputs = model(features) # 前向传播
        loss = criterion(outputs, labels)  # 计算损失
        loss.backward() # 反向传播
        optimizer.step()  # 更新权重
    # 打印每个epoch的损失
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')


