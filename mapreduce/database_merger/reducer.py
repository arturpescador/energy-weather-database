import sys
import datetime

def to_float(s):
    try:
        return float(s)
    except ValueError:
        return float("nan")

def main():
    for line in sys.stdin:
        key, value = line.strip("\n").split("@")
        items = value.split(";")

        IEA_mean_idx = [2]
        IEA_means = [0] * 1
        IEA_nb = 0
        WEATHER_mean_idx = [3, 4, 5]
        WEATHER_means = [0] * 3
        WEATHER_nb = 0
        for item in items:
            li = item.split(",")

            if li[0] == "0":
                for i, j in enumerate(IEA_mean_idx):
                    IEA_means[i] += to_float(li[j])
                IEA_nb += 1
            else:
                for i, j in enumerate(WEATHER_mean_idx):
                    WEATHER_means[i] += to_float(li[j])
                WEATHER_nb += 1

        for i in range(len(IEA_means)):
            IEA_means[i] = str(IEA_means[i] / max(IEA_nb, 1))

        for i in range(len(WEATHER_means)):
            WEATHER_means[i] = str(WEATHER_means[i] / max(WEATHER_nb, 1))

        print(",".join(key.split("_") + IEA_means + WEATHER_means), flush = True)

if __name__ == "__main__":
    main()
