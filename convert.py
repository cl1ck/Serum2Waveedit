from osc_gen import wavetable, dsp, sig, visualize, wavfile
import scipy.io.wavfile
import scipy.signal
import numpy as np
import os
import io
import struct
import sys

SAMPLE_RATE = 44100
SERUM_WAVE_LENGTH = 2048
WAVEEDIT_WAVE_LENGTH = 256
WAVEEDIT_NUM_SLOTS = 64
AMPLITUDE = np.iinfo(np.int16).max


def read_clm_header(input_filename):
    with io.open(input_filename, 'rb') as fh:
        riff, size, file_format = struct.unpack('<4sI4s', fh.read(12))
        chunk_header = fh.read(8)
        chunk_id, chunk_size = struct.unpack('<4sI', chunk_header)

        # skip format header
        if chunk_id == b'fmt ':
            fh.read(16)

        chunk_offset = fh.tell()
        while chunk_offset < size:
            fh.seek(chunk_offset)
            sub_chunk_id, sub_chunk_size = struct.unpack('<4sI', fh.read(8))
            if sub_chunk_id == b'clm ':
                return fh.read(sub_chunk_size).decode('ascii')

            chunk_offset = chunk_offset + sub_chunk_size + 8

        raise TypeError('Input file is not a Serum wavetable!')


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
    clm_header = read_clm_header(input_filename)
    wave_len = int(clm_header[3:7])
    num_slots = int(len(serum_wav) / wave_len)
    wav16 = np.int16(np.clip(serum_wav, -1, 1) * AMPLITUDE)

    if os.path.isfile(temp_filename):
        os.remove(temp_filename)
    wavfile.write(wav16, temp_filename, SAMPLE_RATE)
    table = wavetable.WaveTable(num_slots, wave_len=wave_len).from_wav(temp_filename, resynthesize=False)
    os.remove(temp_filename)

    return table


def convert_serum_to_waveedit(serum_filename):
    # get 64 waves evenly selected from the input wavetable
    input_table = convert_wav_to_16bit(serum_filename)
    idx = np.round(np.linspace(0, len(input_table.waves) - 1, WAVEEDIT_NUM_SLOTS)).astype(np.int16)
    selected_waves = list(np.array(input_table.waves)[idx])

    # downsample to 256 samples per wave
    downsampling_factor = np.round(input_table.wave_len / WAVEEDIT_WAVE_LENGTH).astype(int)
    downsampled_waves = [downsample(samples, downsampling_factor) for samples in selected_waves]

    # save as waveedit bank
    filename, file_extension = os.path.splitext(serum_filename)
    output_filename = filename + '_converted' + file_extension
    save_as_waveedit(downsampled_waves, output_filename)

    return output_filename


def plot_waveedit_file(wav_filename):
    filename, file_extension = os.path.splitext(wav_filename)
    png_filename = filename + '.png'
    visualize.plot_wavetable(
        wavetable.WaveTable(WAVEEDIT_NUM_SLOTS, wave_len=WAVEEDIT_WAVE_LENGTH)
                 .from_wav(wav_filename, resynthesize=False),
        title=filename,
        save=png_filename
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: {0} SERUM_WAV_FILE".format(sys.argv[0]))
        exit()

    converted_filename = convert_serum_to_waveedit(sys.argv[1])
    plot_waveedit_file(converted_filename)


if __name__ == '__main__':
    main()
