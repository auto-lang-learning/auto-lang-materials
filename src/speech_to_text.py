import whisper
import os
import torch 
from typing import TextIO
import time

import whisper.tokenizer


class SpeechToText:
    def __init__(self,model_name='turbo',device=None):
        self.device = device
        if self.device is None:
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
    import subprocess

    def preview_with_subtitles(media_path, generated_subtitle_path, original_subtitle_path=None):
        """
        Preview media file with generated and original subtitles using mpv player
        """
        # Basic command with generated subtitles
        command = ['mpv', 
                  media_path, 
                  '--sid=1',
                  '--sub-file=' + generated_subtitle_path,
                  '--sub-color=1.0/0.0/0.0']  # Yellow for generated subs
        
        if original_subtitle_path and os.path.exists(original_subtitle_path):
            # Add original subtitles as secondary track
            command = ['mpv', 
                        media_path, 
                        '--secondary-sid=2',
                        '--sub-files='+original_subtitle_path+':'+generated_subtitle_path,
                        '--sub-color=1.0/0.0/0.0', # Yellow for generated subs
                        '--secondary-sub-visibility=yes']  
        print("Command to run:")
        print(' '.join(command))
        
        try:
            subprocess.run(command)
        except FileNotFoundError:
            print("Error: mpv player not found. Install with: sudo apt install mpv")

    test_audio = "downloads/test.mp3"
    result_path = "downloads/"
    original_subtitle_path = None
    if not os.path.exists(result_path):
        open(result_path, 'w').close()

    stt = SpeechToText(model_name='turbo',device='cpu')
    start_time = time.time()
    stt.speech_to_text(test_audio, result_path, format='VTT',language=None)
    print("Execution time for transcribe: ", time.time()-start_time)
     # Preview the results
    generated_subs = os.path.join(result_path, os.path.splitext(os.path.basename(test_audio))[0] + '.vtt')
    preview_with_subtitles(test_audio, generated_subs,original_subtitle_path)