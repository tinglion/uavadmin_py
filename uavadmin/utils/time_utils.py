from datetime import datetime, timedelta


def time_str_to_millis(time_str):
    # 分割时间字符串
    s, ms = time_str.split(".")

    segs = s.split(":")
    hours = int(segs[0])
    minutes = int(segs[1])
    seconds = int(segs[2])

    millis = int(ms)
    if len(ms) == 1:
        millis = int(ms) * 100

    total_millis = (
        hours * 60 * 60 * 1000 + minutes * 60 * 1000 + seconds * 1000 + millis
    )
    return total_millis


if __name__ == "__main__":
    time_str = "15:46:56.2"
    millis = time_str_to_millis(time_str)
    print(f"时间 {time_str} 对应的毫秒数是: {millis}")
