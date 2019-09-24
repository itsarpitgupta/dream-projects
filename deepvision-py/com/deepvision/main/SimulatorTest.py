import queue

from com.deepvision.job.JobLoader import JobLoader
from com.deepvision.simulator.ImageLoaderThread import ImageLoaderThread
from com.deepvision.simulator.ImageProcessorThread import ImageProcessorThread
from com.deepvision.simulator.ImageResultThread import ImageResultThread
from concurrent.futures import ThreadPoolExecutor

from deepvision.simulator import ImageServer


def main():
    job_loader = JobLoader()
    job_loader.loadJob()

    processing_queue = queue.Queue(maxsize=1)

    result_queue = queue.Queue(maxsize=10)

    connection = ImageServer.connect()

    image_loader_thread = ImageLoaderThread("ILT", processing_queue)
    # image_loader_thread.setDaemon(True)

    image_processor_thread = ImageProcessorThread(image_process_queue=processing_queue,
                                                  image_result_queue=result_queue, name="IPT",
                                                  tools=job_loader.tool_list, result_dict=job_loader.result_dict,
                                                  job_loader=job_loader)
    # image_processor_thread.setDaemon(True)

    image_result_thread = ImageResultThread(result_queue=result_queue, name="IRT", connection=connection)

    image_result_thread.start()
    image_loader_thread.start()
    image_processor_thread.start()

    # connection.close()
    # image_loader_thread.join()
    # image_processor_thread.join()
    # image_result_thread.join()


if __name__ == "__main__":
    main();
