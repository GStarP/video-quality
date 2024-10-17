# VMAF

[VMAF](https://github.com/Netflix/vmaf) 能够比较 目标视频 和 参考视频 的相似度，并给出数值评分（0~1）

## 实验

### 录制

视频内容为已编排好自动播放的 PPT，开头添加了一个空白页，便于后续截取视频进行对齐。

参考视频和目标视频分别设定为“共享屏幕时发送端本地的视频内容”和“共享屏幕时接收端观看的视频内容”。

1. 放映 PPT
2. 发送端进入会议，选择 PPT 放映窗口进行屏幕共享。
3. 通过开发者工具对屏幕共享的 video 元素执行 $0.requestFullScreen() 全屏，避免 UI 控件干扰。
4. 通过 OBS 录制窗口，录制全屏化的 video 元素。
5. 通过点击开始 PPT 的自动放映，放映完成后结束 OBS 录制。

对接收端也是同样的流程，区别在于必须用另一个接收端进入会议，对接收到屏幕共享内容的 video 元素进行录制。

录制完成后得到 local.mp4 和 remote.mp4，对它们进行剪辑，确保开头的空白页和最后的黑屏被去除，同时尽量保证两个文件时长相近（无论如何一定要确保参考视频的长度更长）

### 评分

执行 `ffmpeg -i local.mp4 -pix_fmt yuv420p local.y4m` 将视频转化为原始像素格式。

执行 `vmaf -r ../assets/local.y4m -d ../assets/remote.y4m --csv -o ../results/vmaf.csv --threads 4` 运行 vmaf 评测工具。命令行会输出一个总体评分。
