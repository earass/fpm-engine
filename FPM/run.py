from pokec.data import DataInterface, Preprocess
from pokec.engine import FPM
from pokec.explore import Explore


if __name__ == '__main__':
    read_sample = True
    di = DataInterface()
    df = di.read(read_sample)

    pr = Preprocess(data=df)
    pr.run()

    df = pr.out

    fpm = FPM(df)
    fpm.run()

    exp = Explore()
    exp.run()
