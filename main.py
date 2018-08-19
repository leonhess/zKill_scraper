import datetime
import logging

from redisq import RedisQ
from killmail import Killmail


def main():
    # just some performance metrics
    start = datetime.datetime.now()
    last100_processing_time = []
    counter = 1

    # logger stuff
    logging.basicConfig(filename='zKill_scraper_{}.log'.format(start), level=logging.DEBUG,
                        format='%(asctime)s %(name)s:%(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    while True:
        unprocessed_killmail = RedisQ.makeCall(RedisQ())
        then = datetime.datetime.now()

        killmail = Killmail(unprocessed_killmail)

        now = datetime.datetime.now()
        processing_time = now - then

        if len(last100_processing_time) > 100:
            last100_processing_time.pop(0)
        last100_processing_time.append(processing_time.total_seconds())
        avg_processing_time = sum(last100_processing_time) / len(last100_processing_time)

        counter = counter + 1

        logger.info("Counter: {}".format(counter))
        logger.info("Processing Time: {}".format(processing_time))
        logger.info("Avg Processing Time: {}".format(avg_processing_time))


if __name__ == "__main__":
    main()