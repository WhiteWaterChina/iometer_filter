# iometer_filter
1. 此工具对windows下Iometer测试结果进行过滤。只针对每个worker都选择所有盘符的情况，这种情况生成的结果比较分散，不容易统一观察。经过这个工具过滤之后能快速分析结果。
2. 使用方法，用pyinstaller制作成exe可执行文件。python pyinstaller.py -F iomter_filter.py
