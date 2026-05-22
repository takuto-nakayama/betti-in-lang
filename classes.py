import stanza


class Text:
	def __init__(self, path:str, lang:str):
		with open(path, mode='r', encoding='utf-8') as f:
			self.text = f.readlines()
			self.parser = stanza.Pipeline(lang, processors='tokenize,pos', tokenize_no_ssplit=True)


	def window_for_word(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed = self.parser(snt)
			words = parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.text for w in words[i:i+k]]
				)

		return windowed_text


	def window_for_chr(self, k:int=5):
		windowed_text = []

		for snt in self.text:
			for i in range(len(snt)-k+1):
				windowed_text.append(tuple(snt[i:i+k]))
			
		return windowed_text


	def window_for_upos(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed = self.parser(snt)
			words = parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.upos for w in words[i:i+k]]
				)

		return windowed_text


	def window_for_xpos(self, k:int=5):
		windowed_text = []		
		for snt in self.text:
			parsed = self.parser(snt)
			words = parsed.sentences[0].words
			for i in range(len(words)-k+1):
				windowed_text.append(
					[w.xpos for w in words[i:i+k]]
				)

		return windowed_text



class WordManifold:
	def __init__(self):
		pass