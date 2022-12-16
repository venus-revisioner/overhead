from typing import Literal
from codex_chat_helpers import ChatHelpers
from codex_class import CodexSmall


class ChatBotsTalking:
    def __init__(self, starter=None, definition=None, continuous_save=True, overwrite=False, load=None) -> None:

        self.command_list: tuple[Literal['help'], Literal['info'], Literal['commands'], Literal['stats'],
        Literal['debug'], Literal['set_definition'], Literal['get_definition'], Literal['parameters'],
        Literal['/exit'], Literal['/start'], Literal['/stop'], Literal['/pause']] \
            = ('help', 'info', 'commands', 'stats', 'debug',
                             'set_definition', 'get_definition', 'parameters',
                             '/exit', '/start', '/stop', '/pause')

        self.bot1 = None
        self.subject_1_name = None
        self.subject_2_name = None
        self.human_writes: None = None

        self.starter = starter
        self.definition = definition
        self.overwrite = overwrite
        self.continuous_save: bool = continuous_save
        self.load_file = load
        self.helper: ChatHelpers = ChatHelpers(starter, definition, continuous_save, overwrite, load)
        self.bot1_name: Literal['bot1'] = "bot1"
        self.bot2_name: Literal['bot2'] = "bot2"

        self.pause_flag: Literal[False] = False

        if self.subject_1_name is None:
            self.subject_1_name: Literal['bot1'] = self.bot1_name

        if self.subject_2_name is None:
            self.subject_2_name: Literal['bot2'] = self.bot2_name

        self.helper.subject_1_name, self.helper.subject_2_name = self.subject_1_name, self.subject_2_name

    def bot2human_async(self) -> None:
        self.helper.subject_1_name = self.subject_1_name
        self.helper.subject_2_name = self.subject_2_name

        self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)

        # create a chatbot
        self.bot1: CodexSmall = CodexSmall(engine="code-davinci-002", temperature=0.994, max_tokens=64, top_p=1,
                               stop_str="\n", frequency_penalty=0.2, presence_penalty=0.1)

        # --------------------------------------------------------------------#
    def wait_user_input(self, update) -> None:
        # if update.message and update.message.text:
        user_comment = self.bot1.sanitize(update.message.text)
        user_name = update.message.from_user.username
        if update.message.from_user["first_name"] is not None:
            user_name = update.message.from_user["first_name"]
        if update.message.from_user["last_name"] is not None:
            user_name += " " + update.message.from_user["last_name"]
        user_name = update.message.chat[''] + f'{ update.message["message_id"]}: ' + update.message.from_user[
            "first_name"] + " " + update.message.from_user["last_name"]
        print(f'{user_name}: {user_comment}')
        self.helper.make_bot_comment(user_comment, str(user_name), end="\n", save_to_file=True, verbose=False)
        self.helper.paragraph_popper()

    def answer_user_input(self, update=None) -> str:
        # use codex to give short answer, use whole discussion (limited by max tokens and rate of query)
        self.bot1.prompt = self.helper.conversation + f"{self.subject_1_name}: "
        bot_response: str|None = self.bot1.completion()
        self.helper.paragraph_popper()
        self.helper.make_bot_comment(bot_response, self.subject_1_name, end="\n\n", save_to_file=True, verbose=False)
        print(f"{self.subject_1_name}: {bot_response}")
        return bot_response
    # --------------------------------------------------------------------#


    def options(self, comment=None) -> str:

        # truth_command = [comment == command for command in self.command_list]
        #
        # if any(truth_command):

        if comment == "commands":
            return f'Available commands: {self.command_list}'

        if comment == "help":
            s: dict[str, str] = self.helper.info()
            return s, "\n" + f'Available commands: {self.command_list}'

        if comment == "info":
            return self.helper.info()

        if comment == "stats":
            return self.helper.conversation_info()

        if comment == "debug":
            print("Prompt: ", self.bot1.prompt)
            print("Conversation: ", self.helper.conversation_info)
            return self.bot1.prompt

        if comment == "set_definition":
            return self.helper.set_definition(comment)

        if comment == "get_definition":
            return self.helper.definition

        if comment == "/exit":
            print("exit program...")
            exit()

        if comment == "parameters":
            # return self.change_parameters(self.bot1)
            t = self.bot1.__dict__['temperature']
            max_tokens = self.bot1.__dict__['max_tokens']
            freq_pen = self.bot1.__dict__['frequency_penalty']
            pres_pen = self.bot1.__dict__['presence_penalty']
            return f"temperature: {t}, max_tokens: {max_tokens}, frequency_penalty: {freq_pen}, presence_penalty: {pres_pen}"

        # --------------------------------------------------------------------#

    def help_info(self) -> None:
        print(self.helper.info())
        print(f'Available commands: {self.command_list}')

    def parameters(self, bot) -> str:
        bot: CodexSmall = self.bot1
        t = bot.__dict__['temperature']
        max_tokens = bot.__dict__['max_tokens']
        freq_pen = bot.__dict__['frequency_penalty']
        pres_pen = bot.__dict__['presence_penalty']
        param_str = f"temperature: {t}, max_tokens: {max_tokens}, frequency_penalty: {freq_pen}, presence_penalty: {pres_pen}"
        print(param_str)
        return param_str


    # def change_parameters(self, bot1, **kwargs):
    #
    #     t = self.bot1.__dict__['temperature']
    #     max_tokens = self.bot1.__dict__['max_tokens']
    #     freq_pen = self.bot1.__dict__['frequency_penalty']
    #     pres_pen = self.bot1.__dict__['presence_penalty']
    #
    #     print(f"temperature: {t}")
    #     self.send_message_to_chat(send_this_text="temperature: {t}", **kwargs)
    #     i = input('Change: y/n? ')
    #     if i == 'y':
    #         t = float(input('New temperature: '))
    #         bot1.temperature = t
    #         print(f"temperature: {t}")
    #
    #     print(f"max_tokens: {max_tokens}")
    #     i = input('Change: y/n? ')
    #     if i == 'y':
    #         max_tokens = int(input('New max_tokens: '))
    #         bot1.max_tokens = max_tokens
    #         print(f"max_tokens: {max_tokens}")
    #
    #     print(f"frequency_penalty: {freq_pen}")
    #     i = input('Change: y/n? ')
    #     if i == 'y':
    #         freq_pen = float(input('New frequency_penalty: '))
    #         bot1.frequency_penalty = freq_pen
    #         print(f"frequency_penalty: {freq_pen}")
    #
    #     print(f"presence_penalty: {pres_pen}")
    #     i = input('Change: y/n? ')
    #     if i == 'y':
    #         pres_pen = float(input('New presence_penalty: '))
    #         bot1.presence_penalty = pres_pen
    #         print(f"presence_penalty: {pres_pen}")
    #






# chatbots = ChatBotsTalking()
# chatbots.helper.set_file_path("bot2human.txt")
# chatbots.helper.subject_2_name = "human"
# chatbots.bot2human_async(starter=3, pause=10)