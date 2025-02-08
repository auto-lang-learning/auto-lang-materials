import whisper
import os
import torch 
from typing import TextIO

import whisper.tokenizer


class SpeechToText:
    def __init__(self,model_name='turbo'):
        if torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        self.model = whisper.load_model(model_name, device=self.device)
    
    def speech_to_text(self, audio_path,output_dir,format='TXT',language=None):
        # Load the audio file
        audio = whisper.load_audio(audio_path)
        result= self.model.transcribe(audio,verbose=True,language=language)
        
        if format=='TXT':
            whisper.utils.WriteTXT(output_dir)(result,audio_path)
        elif format=='SRT':
            whisper.utils.WriteSRT(output_dir)(result, audio_path)
        elif format=='VTT':
            whisper.utils.WriteVTT(output_dir)(result, audio_path)
        elif format=='JSON':
            whisper.utils.WriteJSON(output_dir)(result, audio_path)
        elif format=='TSV':
            whisper.utils.WriteTSV(output_dir)(result, audio_path)


if __name__ == "__main__":
    test_audio = "downloads/test_1min.mp3"
    result_path = "downloads/"
    if not os.path.exists(result_path):
        open(result_path, 'w').close()

    stt = SpeechToText(model_name='large')
    stt.speech_to_text(test_audio, result_path, format='VTT',language='ru')
