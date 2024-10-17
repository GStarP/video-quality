# SSIM

[SSIM](https://en.wikipedia.org/wiki/Structural_similarity_index_measure) 用于比较两张图片的结构相似性，并给出数值评分（0~1）

对于视频相似度，我们可以提取出对应帧的图像计算 SSIM，最后针对所有帧的结果取平均。

## 实验

1、录制参考和目标视频，要求分辨率、帧率相同。

2、执行 `ffmpeg -i ref.mp4 ref/%d.jpg` 将录制下来的视频转化为一系列帧图像。

3、检查这些图像，将开头和结尾无用的部分删去（不需要更改剩余图像的文件名）

4、修改脚本中参数，执行脚本。
