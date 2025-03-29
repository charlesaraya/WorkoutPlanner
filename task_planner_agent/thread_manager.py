class ThreadDB:
    def __init__(self):
        self.__num_threads = 0
        self.threads = []

    def add(self, id="user_session"):
        if id == "user_session":
            id = id + f"_{self.__num_threads}"
        if id not in self.threads:
            self.threads.append(id)
            self.__num_threads += 1
        return id
