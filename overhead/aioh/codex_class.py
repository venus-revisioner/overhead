import os
import time

import openai
import overhead.stringoh


def import_file(filepath):
    with open(filepath, 'r') as file:
        query = file.read()
    return query


class CodexClass:
    def __init__(self, temp=0.6, tokens=256, p=1, stop_str="\n\n\n", verbose=0):

        self.filepath = None
        _key = os.getenv("OPENAI_API_KEY").strip("'")
        openai.api_key = _key
        self.prompt, self.response, self.answer = "", "", ""
        self.temperature = temp
        self.max_tokens = tokens
        self.top_p = p
        self.stop = stop_str
        self.verbose = verbose
        self.engine = "code-davinci-001"
        # self.engine = "code-davinci-002"
        # self.engine = "code-davinci-003"
        # self.engine = "code-cushman-001"
        # self.engine = "code-cushman-002"
        # self.engine = "code-davinci-edit-001"
        # self.engine = "code-cushman-001"
        # self.engine = "text-similarity-babbage-001"
        self.current_path = os.getcwd()
        self.out_file = None
        self.out_file_continued = "codex_class_output.txt"
        self.out_file_path = f'{self.current_path}\\{self.out_file}'
        self.del_chars_alphanum = q
        self.del_chars_smaller = "#$&\'/_()*+:;<=>[]^`{|}~'" + '"'

    # self.del_char_smaller = "'\'"

    def prompt_from_file(self, f=None):
        if not f:
            f = self.filepath
        self.prompt = import_file(f)

    def completion(self, s=None, verbose=0):
        if s is not None:
            self.prompt = s
        if self.prompt is None:
            print("No prompt given.")
            return None
        try:
            self.response = openai.Completion.create(engine=self.engine, prompt=self.prompt,
                                                     temperature=self.temperature, max_tokens=self.max_tokens,
                                                     top_p=self.top_p, logprobs=0,
                                                     frequency_penalty=0, presence_penalty=0, stop=self.stop
                                                     )

            if verbose:
                print("*" * 40)
                print("Choices:", len(self.response['choices']))
                print(self.response)
                print("*" * 40)

            self.answer = self.response['choices'][0]['text']

            if verbose:
                print(self.answer)

            return self.answer

        except Exception as e:
            print(e)

        except KeyboardInterrupt:
            print("\nKeyboard interruption...\n")
            self.ask_if_save(self.prompt)

    def continue_completion(self, s=None, verbose=0):
        if self.prompt is None:
            self.prompt = s
            if s is None:
                print("No prompt given.")
                return None
        self.prompt = self.sanitize(self.prompt)
        self.prompt = self.prompt + self.answer
        self.completion(self.prompt, verbose)

        if verbose:
            print(self.prompt)
            print(self.answer)

        return self.prompt, self.answer

    def ask_if_save(self, s):
        print(f'\nDo you want to save this discussion?\n')
        save_question = input("y/n?: ")
        if save_question in "yY, yes":
            with open(self.out_file_path, "w") as f:
                f.write(s)
            print(f'Discussion saved to "{self.out_file_path}".')
            exit()

    def save(self, s):
        self.out_file = s
        self.out_file_path = f'{self.current_path}\\{self.out_file}'

    def save_continued(self, s):
        self.out_file_continued = s
        self.out_file_path = f'{self.current_path}\\{self.out_file_continued}'
        with open(self.out_file_path, "+a") as f:
            f.write(self.prompt)
            f.write(self.answer)
        print(f'Discussion saved to "{self.out_file_path}".')

    def sanitize(self, s=None):
        if not s:
            s = self.answer

        return [s.replace(i, "") for i in self.del_chars_smaller][0]

    def sanitize_non_alphanum(self, s=None):  # remove non-alphanumeric characters
        if not s:
            s = self.answer
        return s.translate(str.maketrans('', '', self.del_chars_alphanum))

    def answers(self):
        print(self.answer)
        return self.answer

    def print_parameters(self):
        f = f'{self.temperature, self.max_tokens, self.top_p, self.stop}'
        print(f)

    def set_parameters(self, temp=0.6, tokens=256, p=1, stop_str="\n\n\n"):
        self.temperature = temp
        self.max_tokens = tokens
        self.top_p = p
        self.stop = stop_str

    def set_file(self, f):
        self.filepath = f

    def set_out_file(self, f):
        self.out_file = f
        self.out_file_path = f'{self.current_path}\\{self.out_file}'

    def set_engine(self, e):
        self.engine = e

    def set_verbose(self, v):
        self.verbose = v

    def set_prompt(self, s):
        self.prompt = s

    def __repr__(self):
        return f'{self.temperature, self.max_tokens, self.top_p, self.stop}'

    def __str__(self):
        return f'{self.temperature, self.max_tokens, self.top_p, self.stop}'


class CodexSmall:
    def __init__(self, engine, temperature=0.6, max_tokens=256, top_p=1,
                 stop_str="\n\n", frequency_penalty=0.2, presence_penalty=0.2):
        _key = os.getenv("OPENAI_API_KEY").strip("'")
        openai.api_key = _key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stop = stop_str
        self.engine = engine
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.prompt = ""
        self.response = ""
        self.answer = ""
        self.verbose = 0
        self.filepath = None
        self.exception_string = None
        self.quit_flag = False
        self.del_chars_alphanum = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
        self.del_chars_smaller = '"#$&\\/_"()*+;<=>[]^`{|}~""'"" + "\t\b\r\f\v"

    def prompt_from_file(self, f=None):
        if not f:
            f = self.filepath
        self.prompt = import_file(f)

    def continuous_save_to_file(self, s, f=None):
        if not f:
            f = self.filepath
        with open(f, "+a") as f:
            f.write(s)

    def completion(self):
        # lets update to the most recent prompt choices
        # self.prompt = self.prompt + self.answer
        try:
            self.response = openai.Completion.create(engine=self.engine, prompt=self.prompt,
                                                     temperature=self.temperature, max_tokens=self.max_tokens,
                                                     top_p=self.top_p, # logprobs=1,
                                                     frequency_penalty=self.frequency_penalty,
                                                     presence_penalty=self.frequency_penalty, stop=self.stop)

            self.answer = self.response['choices'][0]['text']

        except Exception as e:
            self.exception_string = e
            print(self.exception_string)

            if "token" in str(self.exception_string):
                print("Token limit exceeded. Reduce your prompt")
                # print("Exiting...")
                # self.quit_flag = True
                # exit()
                time.sleep(10)
                

            if "Rate" in str(self.exception_string):
                print("Rate limit exceeded. Wait a few seconds...")
                time.sleep(10)
                self.completion()

        except KeyboardInterrupt:
            print("\nKeyboard interruption...\n")
            return None

        if self.answer is None:
            print("No answer returned...")

        if self.answer is not None:
            return self.sanitize(self.answer)

    def continue_completion(self, s=None, verbose=0):
        if self.prompt is None:
            self.prompt = s
            if s is None:
                print("No prompt given.")
                return None
        self.prompt = self.sanitize(self.prompt)
        self.answer = self.sanitize(self.answer)
        self.prompt = self.prompt + self.answer + "\n"
        self.completion()

        if verbose:
            print(self.prompt)
            print(self.answer)

        self.answer = self.sanitize(self.answer)
        self.prompt = self.sanitize(self.prompt)

        return self.prompt, self.answer

    def sanitize(self, s=None):
        if not s:
            s = self.answer
        return s.translate(str.maketrans('', '', self.del_chars_smaller))

    def sanitize_non_alphanum(self, s=None):  # remove non-alphanumeric characters
        if not s:
            s = self.answer
        return s.translate(str.maketrans('', '', self.del_chars_alphanum))

    def answers(self):
        print(self.answer)
        return self.answer

    def print_parameters(self):
        f = f'{self.temperature, self.max_tokens, self.top_p, self.stop}'
        print(f)

    def set_parameters(self, temp=0.6, tokens=256, p=1, stop_str="\n\n\n"):
        self.temperature = temp
        self.max_tokens = tokens
        self.top_p = p
        self.stop = stop_str

    def set_file(self, f):
        self.filepath = f

    def set_engine(self, e):
        self.engine = e

    def set_verbose(self, v):
        self.verbose = v

    def set_prompt(self, s):

        self.prompt = s

    def __repr__(self):
        return f'{self.temperature, self.max_tokens, self.top_p, self.stop}'

    def __str__(self):
        return f'{self.temperature, self.max_tokens, self.top_p, self.stop}'



# -------------------------------------------------------------------------------------------------

class ChatBotsTalking:
    def __init__(self, starter=None, definition=None, continuous_save=True, overwrite=False, load=None):

        self.command_list = ('help', 'info', 'commands', 'stats', 'debug',
                             'set_definition', 'get_definition', 'parameters', 'exit')

        self.bot1 = None
        self.subject_1_name = None
        self.subject_2_name = None
        self.human_writes = None

        self.starter = starter
        self.definition = definition
        self.overwrite = overwrite
        self.continuous_save = continuous_save
        self.load_file = load
        self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
        self.bot1_name = "bot1"
        self.bot2_name = "bot2"

        if self.subject_1_name is None:
            self.subject_1_name = self.bot1_name

        if self.subject_2_name is None:
            self.subject_2_name = self.bot2_name

        self.helper.subject_1_name, self.helper.subject_2_name = self.subject_1_name, self.subject_2_name


    def bot2bot_improved(self, starter, pause=25):

        self.helper.chat_init_string(starter)  # set the prompt for the chatbots

        # create a chatbot
        bot1 = CodexSmall(engine="code-davinci-002", temperature=0.999, max_tokens=64, top_p=1, stop_str="\n")
        bot2 = CodexSmall(engine="code-davinci-002", temperature=0.99, max_tokens=64, top_p=1, stop_str="\n\n")

        while True:

            self.helper.print_conversation_info()

            # self.helper.add_to_conversation("bot1: ")
            bot1.prompt = self.helper.conversation + "bot1: "
            self.helper.countdown_timer(pause)
            a = bot1.completion()
            self.helper.make_bot_comment(a, "bot1", end="\n", save_to_file=True, verbose=True)

            # self.helper.add_to_conversation("bot2: ")
            bot2.prompt = self.helper.conversation + "bot2: "
            self.helper.countdown_timer(pause)
            b = bot2.completion()
            self.helper.make_bot_comment(b, "bot2", end="\n\n", save_to_file=True, verbose=True)

            if bot1.quit_flag is True or bot2.quit_flag is True:
                break

    def bot2human(self, starter, pause):

        self.helper.chat_init_string(starter)  # set the prompt for the chatbots
        # create a chatbot
        bot1 = CodexSmall(engine="code-davinci-002", temperature=0.9999, max_tokens=128, top_p=1,
                          stop_str="\n", frequency_penalty=0.24, presence_penalty=0.05)

        while True:
            bot1.prompt = self.helper.conversation + "bot1: "
            a = bot1.completion()
            bot_response = self.helper.make_bot_comment(a, "bot1", end="\n", save_to_file=True, verbose=False)
            print(bot_response)
            self.helper.countdown_timer(pause)

            # --------------------------------------------------------------------#

            human_writes = input("human: ")

            if human_writes == "stats":
                self.helper.print_conversation_info()
                # human_writes = input("human: ")

            if human_writes == "debug":
                self.helper.debug()
                # human_writes = input("human: ")

            if human_writes == "parameters":
                self.change_parameters(bot1)
                human_writes = input("human: ")

            if human_writes == "exit":
                break
            if bot1.quit_flag is True:
                break

            self.helper.make_bot_comment(human_writes, "human", end="\n\n", save_to_file=True, verbose=False)

            self.helper.paragraph_popper()
            # self.helper.debug()

            # --------------------------------------------------------------------#


    def bot2human_async(self):
        self.helper.subject_1_name = self.subject_1_name
        self.helper.subject_2_name = self.subject_2_name

        self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)

        # create a chatbot
        self.bot1 = CodexSmall(engine="code-davinci-002", temperature=0.95, max_tokens=64, top_p=1,
                               stop_str="\n", frequency_penalty=0.2, presence_penalty=0.2)

        # --------------------------------------------------------------------#
    def wait_user_input(self, update):
        # if update.message and update.message.text:
        user_comment = self.bot1.sanitize(update.message.text)
        user_name = update.message.from_user["first_name"]
        print(f'{user_name}: {user_comment}')
        self.helper.make_bot_comment(user_comment, str(user_name), end="\n", save_to_file=True, verbose=False)

        self.helper.paragraph_popper()

        if user_comment in self.command_list:
            self.options(user_comment)
    #
    # def command_handler(self, comment):
    #     if comment == "help":
    #         self.helper.help()
    #     if comment == "info":
    #         self.helper.info()
    #     if comment == "commands":
    #         self.helper.commands()
    #     if comment == "stats":
    #         self.helper.print_conversation_info()
    #     if comment == "debug":
    #         self.helper.debug()
    #     if comment == "set_definition":
    #         self.helper.set_definition()
    #     if comment == "get_definition":
    #         self.helper.get_definition()
    #     if comment == "parameters":
    #         self.change_parameters(self.bot1)
    #     if comment == "exit":
    #         self.bot1.quit_flag = True

    def answer_user_input(self, update=None):
        # use codex to give short answer, use whole discussion (limited by max tokens and rate of query)
        self.bot1.prompt = self.helper.conversation + f"{self.subject_1_name}: "



        a = self.bot1.completion()
        bot_response = a
        if bot_response is not None:

            self.helper.make_bot_comment(a, self.subject_1_name, end="\n\n", save_to_file=True, verbose=False)
            print(f"{self.subject_1_name}: {bot_response}")
            return bot_response

        # --------------------------------------------------------------------#


    def options(self, comment=None):
        truth_command = [(comment == command) for command in self.command_list]
        if any(truth_command):
            pass
        else:
            self.answer_user_input(update=None)

        if comment == "commands":
            return f'Available commands: {self.command_list}'

        elif comment == "help":
            s = self.helper.info()
            return s, "\n" + f'Available commands: {self.command_list}'

        elif comment == "info":
            return self.helper.info()

        elif comment == "stats":
            return self.helper.conversation_info()

        elif comment == "debug":
            print("Prompt: ", self.bot1.prompt)
            return self.bot1.prompt + "\n" + self.helper.conversation_info()

        elif comment == "set_definition":
            return self.helper.set_definition(comment)

        elif comment == "get_definition":
            return self.helper.definition

        elif comment == "exit" and len(self.helper.paragraphs(self.helper.conversation)) > 4:
            print("exit program...")
            exit()

        elif comment == "parameters":
            # return self.change_parameters(self.bot1)
            t = self.bot1.__dict__['temperature']
            max_tokens = self.bot1.__dict__['max_tokens']
            freq_pen = self.bot1.__dict__['frequency_penalty']
            pres_pen = self.bot1.__dict__['presence_penalty']
            return f"temperature: {t}, max_tokens: {max_tokens}, frequency_penalty: {freq_pen}, presence_penalty: {pres_pen}"

        # --------------------------------------------------------------------#



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
