import sensor, image, time, os, tf, gc

def calculate_n_most_common(numbers, n):
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    # 按出现次数降序排序，然后取前n个
    most_common_numbers = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:n]
    return most_common_numbers


# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()
results = []
while(True):
    clock.tick()
    img = sensor.snapshot().binary([(0,64)])
    # 数字灰度阈值
    thresholds = [(0, 64)]
    blobs = img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True)
    if len(blobs) == 0:
        continue
    if len(blobs) > 3:
        print("Too many blobs detected") # 防止内存超限
        continue
    for blob in blobs:
        # 对每个blob的区域进行分类
        blob_img = img.crop(roi=blob.rect(), copy=True)
        for obj in tf.classify("trained.tflite", blob_img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
            output = obj.output()
            number = output.index(max(output))
            results.append(number)
        del blob_img
    if len(results) > 90:
        n_most_common_numbers = calculate_n_most_common(results, len(blobs))
        for number, count in n_most_common_numbers:
            print(f"Number: {number}, Count: {count} , Len: {len(blobs)}")
        results = []
    gc.collect()
