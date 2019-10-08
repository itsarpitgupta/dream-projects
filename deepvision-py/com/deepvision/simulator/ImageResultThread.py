import pickle
import threading


class ImageResultThread(threading.Thread):

    def __init__(self, name, result_queue, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.result_queue = result_queue
        self.conn = connection

    def run(self):
        self.display_result()

    def display_result(self):
        while True:
            results = self.result_queue.get()
            results_string = pickle.dumps(results)
            self.conn.send(results_string)
            print('Done send')

            for tool_result in results:
                print('{} - {} - {:.4f}'.format(tool_result.type, tool_result.result, tool_result.time))

                for next_tool_result in tool_result.next_tool:
                    print('{} - {} - {:.4f}'.format(next_tool_result.type, next_tool_result.result,
                                                    next_tool_result.time))

                print('__________________________________________________\n')
