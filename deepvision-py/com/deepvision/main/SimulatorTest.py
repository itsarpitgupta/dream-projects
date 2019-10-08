import queue

from com.deepvision.job.JobLoader import JobLoader
from com.deepvision.simulator.ImageLoaderThread import ImageLoaderThread
from com.deepvision.simulator.ImageProcessorThread import ImageProcessorThread
from com.deepvision.simulator.ImageResultThread import ImageResultThread
from deepvision.io import client_io


def main():
    connection = client_io.connect_to_ui()
    while True:
        command = connection.recv(1024)
        if command.decode('ascii') == 'PLAY':
            start(connection)
        elif command.decode('ascii') == 'STOP':
            print('stop simulator')


def start(connection):
    job_loader = JobLoader()
    job_loader.loadJob()

    processing_queue = queue.Queue(maxsize=1)

    result_queue = queue.Queue(maxsize=10)

    # connection = client_io.connect_to_ui()

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
