import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from skimage import io, img_as_float
from skimage.metrics import structural_similarity as ssim


def compute_ssim(img1: str, img2: str) -> float:
    return ssim(
        img_as_float(io.imread(img1)),
        img_as_float(io.imread(img2)),
        data_range=1.0,
        channel_axis=-1,
    )


###
# 必须将两个视频文件通过 ffmpeg -i x.mp4 x/%d.jpg 转换为一系列帧图像
# 帧图像必须按照顺序排列，但不必关心名称，下标相同的图像将被对比（方便人工对齐）
###
def compare_with_ssim(
    ref_frame_dir: str, des_frame_dir: str, output_file="../results/ssim.csv", threads=4
):
    ref_frames = sorted(os.listdir(ref_frame_dir), key=lambda x: int(x.split(".")[0]))
    des_frames = sorted(os.listdir(des_frame_dir), key=lambda x: int(x.split(".")[0]))

    valid_frame_cnt = min(len(ref_frames), len(des_frames))
    print(f"valid frames: {valid_frame_cnt}")

    result = [-1] * valid_frame_cnt
    counter = 0
    lock = Lock()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        def task_compute_ssim(index: int):
            ref_frame = os.path.join(ref_frame_dir, ref_frames[index])
            des_frame = os.path.join(des_frame_dir, des_frames[index])
            ssim = compute_ssim(ref_frame, des_frame)

            nonlocal counter
            with lock:
                counter += 1
                result[index] = ssim

            sys.stdout.write(f"\rcomputing process: cnt={counter}, ssim={ssim}")
            sys.stdout.flush()

        futures = [executor.submit(task_compute_ssim, i) for i in range(valid_frame_cnt)]
        for _ in as_completed(futures):
            pass

        avg_ssim = sum(result) / valid_frame_cnt

        with open(output_file, "w") as f:
            f.write("frame,ssim\n")
            for i in range(valid_frame_cnt):
                f.write(f"{i},{result[i]}\n")
            f.write(f"avg,{avg_ssim}\n")


compare_with_ssim("../assets/ref", "../assets/des")
