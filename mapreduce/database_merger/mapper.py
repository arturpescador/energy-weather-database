import sys
import datetime

def main():
    for line in sys.stdin:
        value_list = line.strip("\n").split(",")

        dt = datetime.datetime.fromisoformat(value_list[-1])
        dt = dt.replace(hour=dt.hour - (dt.hour % 2))
        
        key = value_list[1] + "_" + dt.strftime("%Y%m%d%H")

        print(key + "@" + ",".join(value_list), flush = True)

if __name__ == "__main__":
    main()
