from osc_gen import wavetable, dsp, sig, visualize, wavfile
import scipy.io.wavfile
import scipy.signal
import numpy as np
import os
from riffreader import WAVFile

SAMPLE_RATE = 44100
SERUM_WAVE_LENGTH = 2048
WAVEEDIT_WAVE_LENGTH = 256
WAVEEDIT_NUM_SLOTS = 64
AMPLITUDE = np.iinfo(np.int16).max


def downsample(samples, downsampling_factor):
    return scipy.signal.decimate(samples, downsampling_factor)


def save_as_waveedit(waves, filename):
    table = wavetable.WaveTable(WAVEEDIT_NUM_SLOTS, wave_len=WAVEEDIT_WAVE_LENGTH)
    table.waves = waves
    if os.path.isfile(filename):
        os.remove(filename)
    table.to_wav(filename, SAMPLE_RATE)


def convert_wav_to_16bit(input_filename):
    filename, file_extension = os.path.splitext(input_filename)
    temp_filename = filename + '_16bit' + file_extension

    rate, serum_wav = scipy.io.wavfile.read(input_filename)
    wave_len = SERUM_WAVE_LENGTH  # todo: read from clm
    num_slots = int(len(serum_wav) / wave_len)
    wav16 = np.int16(np.clip(serum_wav, -1, 1) * AMPLITUDE)

    if os.path.isfile(temp_filename):
        os.remove(temp_filename)
    wavfile.write(wav16, temp_filename, SAMPLE_RATE)
    table = wavetable.WaveTable(num_slots, wave_len=wave_len).from_wav(temp_filename, resynthesize=False)
    os.remove(temp_filename)

    return table


def convert_serum_to_waveedit(serum_filename):
    input_table = convert_wav_to_16bit(serum_filename)
    filename, file_extension = os.path.splitext(serum_filename)
    output_filename = filename + '_converted' + file_extension

    # select 64 slots
    idx = np.round(np.linspace(0, len(input_table.waves) - 1, WAVEEDIT_NUM_SLOTS)).astype(np.int16)
    linspaced_waves = list(np.array(input_table.waves)[idx])

    # downsample to 256 samples per slot
    downsampling_factor = np.round(input_table.wave_len / WAVEEDIT_WAVE_LENGTH).astype(int)
    downsampled_waves = [downsample(samples, downsampling_factor) for samples in linspaced_waves]

    # save as wavetable
    save_as_waveedit(downsampled_waves, output_filename)
    return output_filename


# def main():
#     converted_filename = convert_serum_to_waveedit('serum.wav')
#     visualize.plot_wavetable(
#         wavetable.WaveTable(WAVEEDIT_NUM_SLOTS, wave_len=WAVEEDIT_WAVE_LENGTH)
#             .from_wav(converted_filename, resynthesize=False),
#         title='converted',
#         save='converted.png'
#     )
    wavFile = WAVFile('serum.wav')
    wavFile.read()

if __name__ == '__main__':
    main()
