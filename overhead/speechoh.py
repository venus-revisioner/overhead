from overhead.toolboxoh import print_boxed


class TextToSpeech:
	def __init__(self, rate=140, voice=0, subtitles=0):
		import pyttsx3
		self.voiceover = pyttsx3.init()
		self.rate = rate
		self.voiceover.setProperty('rate', self.rate)
		self.voices = self.voiceover.getProperty('voices')
		self.voice = voice
		self.voiceover.setProperty('voice', self.voices[self.voice].id)
		self.subtitles = subtitles

	def say(self, text, rate=None, voice=None, subtitles=None):
		if subtitles or self.subtitles:
			print(f'Voiceover: "{text}"')

		if rate is not None:
			self.voiceover.setProperty('rate', rate)
		else:
			self.voiceover.setProperty('rate', self.rate)

		if voice is not None:
			self.voiceover.setProperty('voice', self.voices[voice].id)
		else:
			self.voiceover.setProperty('voice', self.voices[self.voice].id)

		self.voiceover.say(text.strip())
		self.voiceover.runAndWait()

	def test_voices(self):
		for enum, v in enumerate(self.voices):
			print(enum)
			self.voiceover.setProperty('rate', 180)
			self.voiceover.setProperty('voice', self.voices[enum].id)
			self.voiceover.say(f'This is a test. I am voice number {enum}')
			self.voiceover.runAndWait()


class SpeechToText:
	"""Example of usage:
		speech = SpeechToText()
		while True:
			a = speech.listen()
			if "exit" in a:
				exit()"""

	def __init__(self, verbose=0, non_speak_dur=0.1, pause_tresh=0.2):
		import speech_recognition as sr
		print_boxed("Initialising speech recognition...")

		self.mic = sr.Microphone()

		self.recog = sr.Recognizer()
		self.recog.adjust_for_ambient_noise(1)
		self.recog.energy_threshold = 300  # minimum audio energy to consider for recording
		self.recog.dynamic_energy_threshold = True
		self.recog.dynamic_energy_adjustment_damping = 0.15
		self.recog.dynamic_energy_ratio = 1.5
		self.recog.pause_threshold = pause_tresh  # seconds of non-speaking audio before a phrase is considered completeself.mic = sr.Microphone()
		self.recog.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
		self.recog.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
		self.recog.non_speaking_duration = non_speak_dur  # seconds of non-speaking audio to keep on both sides of the recordingself.recog.non_speaking_duration = non_speak_dur
		self.recog.pause_threshold = pause_tresh
		self.verbose = verbose

	def listen(self, verbose=None):
		if not verbose:
			verbose = self.verbose
		with self.mic as source:
			if verbose:
				print('Listening...')
			audio = self.recog.listen(source)
			try:
				query = self.recog.recognize_google(audio, language='en-Us')
			except Exception as e:
				print(e)
				return "None"
			if verbose:
				print(f'Recognized: "{query}"')
			return query


class SpeechQuery:
	def __init__(self, query_dict=None):
		self.query_dict = query_dict
		self.talkback = SpeechToText()
		self.voiceover = TextToSpeech(rate=180)

	def ask_me(self, say):
		self.voiceover.say(text=str(say), subtitles=1)
		action = None
		while True:
			answer = self.talkback.listen(verbose=1)
			answer = answer.split(" ")[0]
			if answer in self.query_dict.keys():
				action = self.query_dict[answer][0]
				response = self.query_dict[answer][1]
				self.voiceover.say(response, subtitles=1)
				break
		return action
				# break
