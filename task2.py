import time
import re
from datasketch import HyperLogLog


def load_ips(file_path):
    ips = []
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = ip_pattern.search(line)
                if match:
                    ips.append(match.group(0))
    except FileNotFoundError:
        pass
    return ips


def exact_count(ips):
    return len(set(ips))


def hll_count(ips):
    hll = HyperLogLog(p=14)
    for ip in ips:
        hll.update(ip.encode("utf-8"))
    return hll.count()


if __name__ == "__main__":
    file_path = "lms-stage-access.log"
    ips = load_ips(file_path)

    if not ips:
        print("Помилка: файл логів не знайдено або він порожній.")
    else:
        start_exact = time.time()
        exact_res = exact_count(ips)
        exact_time = time.time() - start_exact

        start_hll = time.time()
        hll_res = hll_count(ips)
        hll_time = time.time() - start_hll

        print("Результати порівняння:")
        print(f"{'':<30}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
        print(
            f"{'Унікальні елементи':<30}{float(exact_res):<20.1f}{float(hll_res):<20.1f}"
        )
        print(f"{'Час виконання (сек.)':<30}{exact_time:<20.5f}{hll_time:<20.5f}")
