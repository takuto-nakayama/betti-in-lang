import stanza


class Text:
	def __init__(self, path:str, lang:str):
		with open(path, mode='r', encoding='utf-8') as f:
			self.text = f.read()
			self.parser = stanza.Pipeline(lang)


	def window_for_word(self, w:int=5):
		windowed_text = []		
		parsed = self.parser(self.text)

		for snt in parsed.sentences:
			for i in range(len(snt.words)-w+1):
				windowed_text.append(
					[w.text for w in snt.words[i:i+w]]
					)
		
		return windowed_text


	def window_for_chr(self, w:int=5):
		windowed_text = []

		for snt in self.text:
			for i in range(len(snt)-w+1):
				windowed_text.append(tuple(snt[i:i+w]))
			
		return windowed_text


	def window_for_upos(self, w:int=5):
		windowed_text = []
		parsed = self.parser(self.text)

		for snt in parsed.sentences:
			for i in range(len(snt.words)-w+1):
				windowed_text.append(
					[w.upos for w in snt.words[i:i+w]]
					)
			
		return windowed_text


	def window_for_xpos(self, w:int=5):
		windowed_text = []
		parsed = self.parser(self.text)

		for snt in parsed.sentences:
			for i in range(len(snt.words)-w+1):
				windowed_text.append(
					[w.xpos for w in snt.words[i:i+w]]
					)
			
		return windowed_text



class WordManifold:
	def __init__(self):
		pass