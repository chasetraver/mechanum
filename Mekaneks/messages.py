class Messages:
    message5: str

    def __init__(self) -> object:
        self.message1 = " "
        self.message2 = " "
        self.message3 = " "
        self.message4 = " "
        self.message5 = " "

    def new_message(self, new):
        if not self.message5 == new and new != "":
            self.message1 = self.message2
            self.message2 = self.message3
            self.message3 = self.message4
            self.message4 = self.message5
            assert isinstance(new, object)
            self.message5 = new

    def new_tutorial_message(self, new):

        if not self.message4 == new and new != "":
            if not self.message3 == new and new != "":
                if not self.message2 == new and new != "":
                    if not self.message1 == new and new != "":
                        self.message1 = self.message2
                        self.message2 = self.message3
                        self.message3 = self.message4
                        self.message4 = new
                        assert isinstance(new, object)
                        self.message5 = "Click anywhere to continue."


    def get_messages(self) -> object:
        return self.message1, self.message2, self.message3, self.message4, self.message5
